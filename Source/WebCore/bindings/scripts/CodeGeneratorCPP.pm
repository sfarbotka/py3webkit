
# Copyright (C) 2005, 2006 Nikolas Zimmermann <zimmermann@kde.org>
# Copyright (C) 2006 Anders Carlsson <andersca@mac.com> 
# Copyright (C) 2006, 2007 Samuel Weinig <sam@webkit.org>
# Copyright (C) 2006 Alexey Proskuryakov <ap@webkit.org>
# Copyright (C) 2006, 2007, 2008, 2009 Apple Inc. All rights reserved.
# Copyright (C) 2009 Cameron McCormack <cam@mcc.id.au>
# Copyright (C) Research In Motion Limited 2010. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public License
# aint with this library; see the file COPYING.LIB.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.
#

package CodeGeneratorCPP;

# Global Variables
my $module = "";
my $outputDir = "";

my @headerContentHeader = ();
my @headerContent = ();
my %headerForwardDeclarations = ();

my @implContentHeader = ();
my @implContent = ();
my %implIncludes = ();

# Constants
my $exceptionInit = "WebCore::ExceptionCode ec = 0;";
my $exceptionRaiseOnError = "webDOMRaiseError(static_cast<WebDOMExceptionCode>(ec));";

# Default License Templates
my $headerLicenseTemplate = << "EOF";
/*
 * Copyright (C) Research In Motion Limited 2010. All rights reserved.
 * Copyright (C) 2004, 2005, 2006, 2007, 2008, 2009 Apple Inc. All rights reserved.
 * Copyright (C) 2006 Samuel Weinig <sam.weinig\@gmail.com>
 * Copyright (C) Research In Motion Limited 2010. All rights reserved.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public License
 * along with this library; see the file COPYING.LIB.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
 * Boston, MA 02110-1301, USA.
 */
EOF

my $implementationLicenseTemplate = << "EOF";
/*
 * This file is part of the WebKit open source project.
 * This file has been generated by generate-bindings.pl. DO NOT MODIFY!
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public License
 * along with this library; see the file COPYING.LIB.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
 * Boston, MA 02110-1301, USA.
 */
EOF

# Default constructor
sub new
{
    my $object = shift;
    my $reference = { };

    $codeGenerator = shift;
    $outputDir = shift;
    shift; # $outputHeadersDir
    shift; # $useLayerOnTop
    shift; # $preprocessor
    shift; # $writeDependencies

    bless($reference, $object);
    return $reference;
}

sub finish
{
    my $object = shift;
}

# Params: 'domClass' struct
sub GenerateInterface
{
    my $object = shift;
    my $dataNode = shift;
    my $defines = shift;

    my $name = $dataNode->name;
    my $className = GetClassName($name);
    my $parentClassName = "WebDOM" . GetParentImplClassName($dataNode);

    # Start actual generation.
    $object->GenerateHeader($dataNode);
    $object->GenerateImplementation($dataNode);

    # Write changes.
    $object->WriteData("WebDOM" . $name);
}

# Params: 'idlDocument' struct
sub GenerateModule
{
    my $object = shift;
    my $dataNode = shift;

    $module = $dataNode->module;
}

sub GetClassName
{
    my $name = $codeGenerator->StripModule(shift);

    # special cases
    return "WebDOMString" if $codeGenerator->IsStringType($name) or $name eq "SerializedScriptValue";
    return "WebDOMObject" if $name eq "DOMObject";
    return "bool" if $name eq "boolean";
    return $name if $codeGenerator->IsPrimitiveType($name);
    return "WebDOMCustomVoidCallback" if $name eq "VoidCallback";

    return "WebDOM$name";
}

sub GetImplClassName
{
    return $codeGenerator->StripModule(shift);
}

sub GetParentImplClassName
{
    my $dataNode = shift;

    if (@{$dataNode->parents} eq 0) {
        return "EventTarget" if $dataNode->extendedAttributes->{"EventTarget"};
        return "Object";
    }

    return $codeGenerator->StripModule($dataNode->parents(0));
}

sub GetParent
{
    my $dataNode = shift;
    my $numParents = @{$dataNode->parents};

    my $parent = "";
    if ($numParents eq 0) {
        $parent = "WebDOMObject";
        $parent = "WebDOMEventTarget" if $dataNode->extendedAttributes->{"EventTarget"};
    } elsif ($numParents eq 1) {
        my $parentName = $codeGenerator->StripModule($dataNode->parents(0));
        $parent = "WebDOM" . $parentName;
    } else {
        my @parents = @{$dataNode->parents};
        my $firstParent = $codeGenerator->StripModule(shift(@parents));
        $parent = "WebDOM" . $firstParent;
    }

    return $parent;
}

sub ShouldSkipTypeInImplementation
{
    my $typeInfo = shift;

    return 1 if $typeInfo->signature->extendedAttributes->{"Custom"}
             and !$typeInfo->signature->extendedAttributes->{"NoCPPCustom"};

    return 1 if $typeInfo->signature->extendedAttributes->{"CustomArgumentHandling"}
             or $typeInfo->signature->extendedAttributes->{"CustomGetter"}
             or $typeInfo->signature->extendedAttributes->{"NeedsUserGestureCheck"}
             or $typeInfo->signature->extendedAttributes->{"CPPCustom"};

    # FIXME: We don't generate bindings for SVG related interfaces yet
    return 1 if $typeInfo->signature->name =~ /getSVGDocument/;

    return 1 if $typeInfo->signature->name =~ /Constructor/;
    return 0;
}

sub ShouldSkipTypeInHeader
{
    my $typeInfo = shift;

    # FIXME: We currently ignore any attribute/function needing custom code
    return 1 if $typeInfo->signature->extendedAttributes->{"CustomArgumentHandling"}
             or $typeInfo->signature->extendedAttributes->{"CustomGetter"};

    # FIXME: We don't generate bindings for SVG related interfaces yet
    return 1 if $typeInfo->signature->name =~ /getSVGDocument/;

    return 1 if $typeInfo->signature->name =~ /Constructor/;
    return 0;
}

sub GetCPPType
{
    my $type = shift;
    my $useConstReference = shift;
    my $name = GetClassName($type);

    return "int" if $type eq "long";
    return "unsigned" if $name eq "unsigned long";
    return "unsigned short" if $type eq "CompareHow";
    return "double" if $name eq "Date";

    if ($codeGenerator->IsStringType($type)) {
        if ($useConstReference) {
            return "const $name&";
        }

        return $name;
    }

    return $name if $codeGenerator->IsPrimitiveType($type) or $type eq "DOMTimeStamp";
    return "const $name&" if $useConstReference;
    return $name;
}

sub ConversionNeeded
{
    my $type = $codeGenerator->StripModule(shift);
    return !$codeGenerator->IsNonPointerType($type) && !$codeGenerator->IsStringType($type);
}

sub GetCPPTypeGetter
{
    my $argName = shift;
    my $type = $codeGenerator->StripModule(shift);

    return $argName if $codeGenerator->IsPrimitiveType($type) or $codeGenerator->IsStringType($type);
    return "static_cast<WebCore::Range::CompareHow>($argName)" if $type eq "CompareHow";
    return "WebCore::SerializedScriptValue::create(WTF::String($argName))" if $type eq "SerializedScriptValue";
    return "to" . GetNamespaceForClass($argName) . "($argName)";
}

sub AddForwardDeclarationsForType
{
    my $type = $codeGenerator->StripModule(shift);
    my $public = shift;

    return if $codeGenerator->IsNonPointerType($type) or $codeGenerator->IsStringType($type);

    my $class = GetClassName($type);
    $headerForwardDeclarations{$class} = 1 if $public;
}

sub AddIncludesForType
{
    my $type = $codeGenerator->StripModule(shift);

    return if $codeGenerator->IsNonPointerType($type);
    return if $type =~ /Constructor/;

    if ($codeGenerator->IsStringType($type)) {
        $implIncludes{"wtf/text/AtomicString.h"} = 1;
        $implIncludes{"KURL.h"} = 1;
        $implIncludes{"WebDOMString.h"} = 1;
        return;
    }

    if ($type eq "DOMObject") {
        $implIncludes{"WebDOMObject.h"} = 1;
        return;
    }

    if ($type eq "EventListener") {
        $implIncludes{"WebNativeEventListener.h"} = 1;
        return;
    }

    if ($type eq "SerializedScriptValue") {
        $implIncludes{"SerializedScriptValue.h"} = 1;
        return;
    }
    
    if ($type eq "VoidCallback") {
        $implIncludes{"WebDOMCustomVoidCallback.h"} = 1;
        return;
    }

    $implIncludes{"Node.h"} = 1 if $type eq "NodeList";
    $implIncludes{"CSSMutableStyleDeclaration.h"} = 1 if $type eq "CSSStyleDeclaration";

    # Default, include the same named file (the implementation) and the same name prefixed with "WebDOM". 
    $implIncludes{"$type.h"} = 1 unless $type eq "DOMObject";
    $implIncludes{"WebDOM$type.h"} = 1;
}

sub GenerateConditionalString
{
    my $node = shift;
    my $conditional = $node->extendedAttributes->{"Conditional"};
    if ($conditional) {
        return $codeGenerator->GenerateConditionalStringFromAttributeValue($conditional);
    } else {
        return "";
    }
}

sub GetNamespaceForClass
{
    my $type = shift;
    return "WTF" if (($type eq "ArrayBuffer") or ($type eq "ArrayBufferView")); 
    return "WTF" if (($type eq "Uint8Array") or ($type eq "Uint16Array") or ($type eq "Uint32Array")); 
    return "WTF" if (($type eq "Int8Array") or ($type eq "Int16Array") or ($type eq "Int32Array")); 
    return "WTF" if (($type eq "Float32Array") or ($type eq "Float64Array"));    
    return "WebCore";
}

sub GenerateHeader
{
    my $object = shift;
    my $dataNode = shift;

    my $interfaceName = $dataNode->name;
    my $className = GetClassName($interfaceName);
    my $implClassName = GetImplClassName($interfaceName);
    
    my $implClassNameWithNamespace = GetNamespaceForClass($implClassName) . "::" . $implClassName;

    my $parentName = "";
    $parentName = GetParent($dataNode);

    my $numConstants = @{$dataNode->constants};
    my $numAttributes = @{$dataNode->attributes};
    my $numFunctions = @{$dataNode->functions};

    # - Add default header template
    @headerContentHeader = split("\r", $headerLicenseTemplate);
    push(@headerContentHeader, "\n#ifndef $className" . "_h");
    push(@headerContentHeader, "\n#define $className" . "_h\n\n");

    my $conditionalString = GenerateConditionalString($dataNode);
    push(@headerContentHeader, "#if ${conditionalString}\n\n") if $conditionalString;

    # - INCLUDES -

    my %headerIncludes = ();
    $headerIncludes{"WebDOMString.h"} = 1;
    $headerIncludes{"$parentName.h"} = 1;
    foreach my $include (sort keys(%headerIncludes)) {
        push(@headerContentHeader, "#include <$include>\n");
    }

    push(@headerContent, "class $className");
    push(@headerContent, " : public $parentName") if $parentName;
    push(@headerContent, " {\n");
    push(@headerContent, "public:\n");

    # Constructor
    push(@headerContent, "    $className();\n");
    push(@headerContent, "    explicit $className($implClassNameWithNamespace*);\n");

    # Copy constructor and assignment operator on classes which have the d-ptr
    if ($parentName eq "WebDOMObject") {
        push(@headerContent, "    $className(const $className&);\n");
        push(@headerContent, "    ${className}& operator=(const $className&);\n");
    }

    # Destructor
    if ($parentName eq "WebDOMObject") {
        push(@headerContent, "    virtual ~$className();\n");
    } else {
        push(@headerContent, "    virtual ~$className() { }\n");
    }

    push(@headerContent, "\n");
    $headerForwardDeclarations{$implClassNameWithNamespace} = 1;

    # - Add constants.
    if ($numConstants > 0) {
        my @headerConstants = ();
        my @constants = @{$dataNode->constants};
        my $combinedConstants = "";

        # FIXME: we need a way to include multiple enums.
        foreach my $constant (@constants) {
            my $constantName = $constant->name;
            my $constantValue = $constant->value;
            my $conditional = $constant->extendedAttributes->{"Conditional"};
            my $notLast = $constant ne $constants[-1];

            if ($conditional) {
                my $conditionalString = $codeGenerator->GenerateConditionalStringFromAttributeValue($conditional);
                $combinedConstants .= "#if ${conditionalString}\n";
            }
            $combinedConstants .= "        WEBDOM_$constantName = $constantValue";
            $combinedConstants .= "," if $notLast;
            if ($conditional) {
                $combinedConstants .= "\n#endif\n";
            } elsif ($notLast) {
                $combinedConstants .= "\n";
            }
        }

        push(@headerContent, "    ");
        push(@headerContent, "enum {\n");
        push(@headerContent, $combinedConstants);
        push(@headerContent, "\n    ");
        push(@headerContent, "};\n\n");
    }

    my @headerAttributes = ();

    # - Add attribute getters/setters.
    if ($numAttributes > 0) {
        foreach my $attribute (@{$dataNode->attributes}) {
            next if ShouldSkipTypeInHeader($attribute);

            my $attributeConditionalString = GenerateConditionalString($attribute->signature);
            my $attributeName = $attribute->signature->name;
            my $attributeType = GetCPPType($attribute->signature->type, 0);
            my $attributeIsReadonly = ($attribute->type =~ /^readonly/);
            my $property = "";
            
            $property .= "#if ${attributeConditionalString}\n" if $attributeConditionalString;
            $property .= "    " . $attributeType . ($attributeType =~ /\*$/ ? "" : " ") . $attributeName . "() const";

            my $availabilityMacro = "";
            my $declarationSuffix = ";\n";

            AddForwardDeclarationsForType($attribute->signature->type, 1);

            $attributeType = GetCPPType($attribute->signature->type, 1);
            my $setterName = "set" . ucfirst($attributeName);

            $property .= $declarationSuffix;
            push(@headerAttributes, $property);
            if (!$attributeIsReadonly and !$attribute->signature->extendedAttributes->{"Replaceable"}) {
                $property = "    void $setterName($attributeType)";
                $property .= $declarationSuffix;
                push(@headerAttributes, $property); 
            }

            push(@headerAttributes, "#endif\n") if $attributeConditionalString;
        }
        push(@headerContent, @headerAttributes) if @headerAttributes > 0;
    }

    my @headerFunctions = ();
    my @deprecatedHeaderFunctions = ();
    my @interfaceFunctions = ();

    # - Add functions.
    if ($numFunctions > 0) {
        foreach my $function (@{$dataNode->functions}) {
            next if ShouldSkipTypeInHeader($function);
            my $functionName = $function->signature->name;

            my $returnType = GetCPPType($function->signature->type, 0);
            my $numberOfParameters = @{$function->parameters};
            my %typesToForwardDeclare = ($function->signature->type => 1);

            my $parameterIndex = 0;
            my $functionSig = "$returnType $functionName(";
            my $methodName = $functionName;
            foreach my $param (@{$function->parameters}) {
                my $paramName = $param->name;
                my $paramType = GetCPPType($param->type, 1);
                $typesToForwardDeclare{$param->type} = 1;

                $functionSig .= ", " if $parameterIndex >= 1;
                $functionSig .= "$paramType $paramName";
                $parameterIndex++;
            }
            $functionSig .= ")";
            if ($dataNode->extendedAttributes->{"PureInterface"}) {
                push(@interfaceFunctions, "    virtual " . $functionSig . " = 0;\n");
            }
            my $functionDeclaration = $functionSig;
            $functionDeclaration .= ";\n";

            foreach my $type (keys %typesToForwardDeclare) {
                # add any forward declarations to the public header if a deprecated version will be generated
                AddForwardDeclarationsForType($type, 1);
            }

            push(@headerFunctions, "    ");
            push(@headerFunctions, $functionDeclaration);
        }

        if (@headerFunctions > 0) {
            push(@headerContent, "\n") if @headerAttributes > 0;
            push(@headerContent, @headerFunctions);
        }
    }

    push(@headerContent, "\n");
    push(@headerContent, "    $implClassNameWithNamespace* impl() const;\n");

    if ($parentName eq "WebDOMObject") {
        push(@headerContent, "\nprotected:\n");
        push(@headerContent, "    struct ${className}Private;\n");
        push(@headerContent, "    ${className}Private* m_impl;\n");
    }

    push(@headerContent, "};\n\n");

    # for PureInterface classes also add the interface that the client code needs to
    # implement
    if ($dataNode->extendedAttributes->{"PureInterface"}) {
        push(@headerContent, "class WebUser$interfaceName {\n");
        push(@headerContent, "public:\n");
        push(@headerContent, "    virtual void ref() = 0;\n");
        push(@headerContent, "    virtual void deref() = 0;\n\n");
        push(@headerContent, @interfaceFunctions);
        push(@headerContent, "\nprotected:\n");
        push(@headerContent, "    virtual ~WebUser$interfaceName() {}\n");
        push(@headerContent, "};\n\n");
    }

    my $namespace = GetNamespaceForClass($implClassName);
    push(@headerContent, "$namespace" . "::$implClassName* toWebCore(const $className&);\n");
    push(@headerContent, "$className toWebKit($namespace" . "::$implClassName*);\n");
    if ($dataNode->extendedAttributes->{"PureInterface"}) {
        push(@headerContent, "$className toWebKit(WebUser$interfaceName*);\n");
    }
    push(@headerContent, "\n#endif\n");
    push(@headerContent, "#endif // ${conditionalString}\n\n") if $conditionalString;
}

sub AddEarlyReturnStatement
{
    my $returnType = shift;

    if (!defined($returnType) or $returnType eq "void") {
        $returnType = "";
    } elsif ($codeGenerator->IsPrimitiveType($returnType)) {
        $returnType = " 0";
    } elsif ($returnType eq "bool") {
        $returnType = " false";
    } else {
        $returnType = " $returnType()";
    }

    # TODO: We could set exceptions here, if we want that
    my $statement = "    if (!impl())\n";
    $statement .=   "        return$returnType;\n\n";
    return $statement;
}

sub AddReturnStatement
{
    my $typeInfo = shift;
    my $returnValue = shift;

    # Used to invoke KURLs "const String&" operator
    if ($codeGenerator->IsStringType($typeInfo->signature->type)) {
        return "    return static_cast<const WTF::String&>($returnValue);\n";
    }

    return "    return $returnValue;\n";
}

sub GenerateImplementation
{
    my $object = shift;
    my $dataNode = shift;

    my @ancestorInterfaceNames = ();

    if (@{$dataNode->parents} > 1) {
        $codeGenerator->AddMethodsConstantsAndAttributesFromParentClasses($dataNode, \@ancestorInterfaceNames);
    }

    my $interfaceName = $dataNode->name;
    my $className = GetClassName($interfaceName);
    my $implClassName = GetImplClassName($interfaceName);
    my $parentImplClassName = GetParentImplClassName($dataNode);
    my $implClassNameWithNamespace = GetNamespaceForClass($implClassName) . "::" . $implClassName;
    my $baseClass = "WebDOM$parentImplClassName";
    my $conditional = $dataNode->extendedAttributes->{"Conditional"};

    my $numAttributes = @{$dataNode->attributes};
    my $numFunctions = @{$dataNode->functions};

    # - Add default header template.
    @implContentHeader = split("\r", $implementationLicenseTemplate);

    # - INCLUDES -
    push(@implContentHeader, "\n#include \"config.h\"\n");
    my $conditionalString = GenerateConditionalString($dataNode);
    push(@implContentHeader, "\n#if ${conditionalString}\n\n") if $conditionalString;
    push(@implContentHeader, "#include \"$className.h\"\n\n");

    $implIncludes{"WebExceptionHandler.h"} = 1;
    $implIncludes{"$implClassName.h"} = 1;
    @implContent = ();

    push(@implContent, "#include <wtf/GetPtr.h>\n");
    push(@implContent, "#include <wtf/RefPtr.h>\n\n");

    # Private datastructure, encapsulating WebCore types
    if ($baseClass eq "WebDOMObject") {
        push(@implContent, "struct ${className}::${className}Private {\n");
        push(@implContent, "    ${className}Private($implClassNameWithNamespace* object = 0)\n");
        push(@implContent, "        : impl(object)\n");
        push(@implContent, "    {\n");
        push(@implContent, "    }\n\n");
        push(@implContent, "    RefPtr<$implClassNameWithNamespace> impl;\n");
        push(@implContent, "};\n\n");
    }

    # Constructor
    push(@implContent, "${className}::$className()\n");
    push(@implContent, "    : ${baseClass}()\n");
    push(@implContent, "    , m_impl(0)\n") if ($baseClass eq "WebDOMObject");
    push(@implContent, "{\n");
    push(@implContent, "}\n\n");

    push(@implContent, "${className}::$className($implClassNameWithNamespace* impl)\n");
    if ($baseClass eq "WebDOMObject") {
        push(@implContent, "    : ${baseClass}()\n");
        push(@implContent, "    , m_impl(new ${className}Private(impl))\n");
        push(@implContent, "{\n");
        push(@implContent, "}\n\n");

        push(@implContent, "${className}::${className}(const ${className}& copy)\n");
        push(@implContent, "    : ${baseClass}()\n");
        push(@implContent, "{\n");
        push(@implContent, "    m_impl = copy.impl() ? new ${className}Private(copy.impl()) : 0;\n");
        push(@implContent, "}\n\n");

        push(@implContent, "${className}& ${className}::operator\=(const ${className}& copy)\n");
        push(@implContent, "{\n");
        push(@implContent, "    delete m_impl;\n");
        push(@implContent, "    m_impl = copy.impl() ? new ${className}Private(copy.impl()) : 0;\n");
        push(@implContent, "    return *this;\n");
        push(@implContent, "}\n\n");

        push(@implContent, "$implClassNameWithNamespace* ${className}::impl() const\n");
        push(@implContent, "{\n");
        push(@implContent, "    return m_impl ? m_impl->impl.get() : 0;\n");
        push(@implContent, "}\n\n");

        # Destructor
        push(@implContent, "${className}::~$className()\n");
        push(@implContent, "{\n");
        push(@implContent, "    delete m_impl;\n");
        push(@implContent, "    m_impl = 0;\n");
        push(@implContent, "}\n\n");
    } else {
        push(@implContent, "    : ${baseClass}(impl)\n");
        push(@implContent, "{\n");
        push(@implContent, "}\n\n");

        push(@implContent, "$implClassNameWithNamespace* ${className}::impl() const\n");
        push(@implContent, "{\n");
        push(@implContent, "    return static_cast<$implClassNameWithNamespace*>(${baseClass}::impl());\n");
        push(@implContent, "}\n\n");
    }

    # START implementation
    %attributeNames = ();

    # - Attributes
    if ($numAttributes > 0) {
        foreach my $attribute (@{$dataNode->attributes}) {
            next if ShouldSkipTypeInImplementation($attribute);
            AddIncludesForType($attribute->signature->type);

            my $idlType = $codeGenerator->StripModule($attribute->signature->type);

            my $attributeName = $attribute->signature->name;
            my $attributeType = GetCPPType($attribute->signature->type, 0);
            my $attributeIsReadonly = ($attribute->type =~ /^readonly/);

            $attributeNames{$attributeName} = 1;

            # - GETTER
            my $getterSig = "$attributeType $className\:\:$attributeName() const\n";
            my $hasGetterException = @{$attribute->getterExceptions};
            my $getterContentHead = "impl()->" . $codeGenerator->GetterExpressionPrefix(\%implIncludes, $interfaceName, $attribute);
            my $getterContentTail = ")";

            # Special cases
            my @customGetterContent = (); 
            if ($attribute->signature->extendedAttributes->{"ConvertToString"}) {
                $getterContentHead = "WTF::String::number(" . $getterContentHead;
                $getterContentTail .= ")";
            } elsif ($attribute->signature->type eq "SerializedScriptValue") {
                $getterContentHead = "$getterContentHead";
                $getterContentTail .= "->toString()";                
            } elsif (ConversionNeeded($attribute->signature->type)) {
                $getterContentHead = "toWebKit(WTF::getPtr($getterContentHead";
                $getterContentTail .= "))";
            }

            my $getterContent;
            if ($hasGetterException) {
                $getterContent = $getterContentHead . "ec" . $getterContentTail;
            } else {
                $getterContent = $getterContentHead . $getterContentTail;
            }

            my $attributeConditionalString = GenerateConditionalString($attribute->signature);
            push(@implContent, "#if ${attributeConditionalString}\n") if $attributeConditionalString;

            push(@implContent, $getterSig);
            push(@implContent, "{\n");
            push(@implContent, AddEarlyReturnStatement($attributeType));
            push(@implContent, @customGetterContent);
            if ($hasGetterException) {
                # Differentiated between when the return type is a pointer and
                # not for white space issue (ie. Foo *result vs. int result).
                if ($attributeType =~ /\*$/) {
                    $getterContent = $attributeType . "result = " . $getterContent;
                } else {
                    $getterContent = $attributeType . " result = " . $getterContent;
                }

                push(@implContent, "    $exceptionInit\n");
                push(@implContent, "    $getterContent;\n");
                push(@implContent, "    $exceptionRaiseOnError\n");
                push(@implContent, AddReturnStatement($attribute, "result"));
            } else {
                push(@implContent, AddReturnStatement($attribute, $getterContent));
            }
            push(@implContent, "}\n\n");

            # - SETTER
            if (!$attributeIsReadonly and !$attribute->signature->extendedAttributes->{"Replaceable"}) {
                # Exception handling
                my $hasSetterException = @{$attribute->setterExceptions};

                my $coreSetterName = "set" . $codeGenerator->WK_ucfirst($attributeName);
                my $setterName = "set" . ucfirst($attributeName);
                my $argName = "new" . ucfirst($attributeName);
                my $arg = GetCPPTypeGetter($argName, $idlType);

                # The definition of ConvertToString is flipped for the setter
                if ($attribute->signature->extendedAttributes->{"ConvertToString"}) {
                    $arg = "WTF::String($arg).toInt()";
                }

                my $attributeType = GetCPPType($attribute->signature->type, 1);
                push(@implContent, "void $className\:\:$setterName($attributeType $argName)\n");
                push(@implContent, "{\n");
                push(@implContent, AddEarlyReturnStatement());

                push(@implContent, "    $exceptionInit\n") if $hasSetterException;
                my $ec = $hasSetterException ? ", ec" : "";
                my $setterExpressionPrefix = $codeGenerator->SetterExpressionPrefix(\%implIncludes, $interfaceName, $attribute);
                push(@implContent, "    impl()->$setterExpressionPrefix$arg$ec);\n");
                push(@implContent, "    $exceptionRaiseOnError\n") if $hasSetterException;
                push(@implContent, "}\n\n");
            }

            push(@implContent, "#endif\n") if $attributeConditionalString;
        }
    }

    # - Functions
    if ($numFunctions > 0) {
        foreach my $function (@{$dataNode->functions}) {
            # Treat PureInterface as Custom as well, since the WebCore versions will take a script context as well
            next if ShouldSkipTypeInImplementation($function) || $dataNode->extendedAttributes->{"PureInterface"};
            AddIncludesForType($function->signature->type);

            my $functionName = $function->signature->name;
            my $returnType = GetCPPType($function->signature->type, 0);
            my $hasParameters = @{$function->parameters};
            my $raisesExceptions = @{$function->raisesExceptions};

            my @parameterNames = ();
            my @needsAssert = ();
            my %needsCustom = ();

            my $parameterIndex = 0;

            my $functionSig = "$returnType $className\:\:$functionName(";
            foreach my $param (@{$function->parameters}) {
                my $paramName = $param->name;
                my $paramType = GetCPPType($param->type, 1);

                # make a new parameter name if the original conflicts with a property name
                $paramName = "in" . ucfirst($paramName) if $attributeNames{$paramName};

                AddIncludesForType($param->type);

                my $idlType = $codeGenerator->StripModule($param->type);
                my $implGetter = GetCPPTypeGetter($paramName, $idlType);

                push(@parameterNames, $implGetter);
                $needsCustom{"NodeToReturn"} = $paramName if $param->extendedAttributes->{"Return"};

                unless ($codeGenerator->IsPrimitiveType($idlType) or $codeGenerator->IsStringType($idlType)) {
                    push(@needsAssert, "    ASSERT($paramName);\n");
                }

                $functionSig .= ", " if $parameterIndex >= 1;
                $functionSig .= "$paramType $paramName";
                $parameterIndex++;
            }

            $functionSig .= ")";

            my @functionContent = ();
            push(@parameterNames, "ec") if $raisesExceptions;
            my $content = "impl()->" . $codeGenerator->WK_lcfirst($functionName) . "(" . join(", ", @parameterNames) . ")"; 

            if ($returnType eq "void") {
                # Special case 'void' return type.
                if ($raisesExceptions) {
                    push(@functionContent, "    $exceptionInit\n");
                    push(@functionContent, "    $content;\n");
                    push(@functionContent, "    $exceptionRaiseOnError\n");
                } else {
                    push(@functionContent, "    $content;\n");
                }
            } elsif (defined $needsCustom{"NodeToReturn"}) {
                # TODO: This is important to enable, once we care about custom code!

                # Special case the insertBefore, replaceChild, removeChild 
                # and appendChild functions from DOMNode 
                my $toReturn = $needsCustom{"NodeToReturn"};
                if ($raisesExceptions) {
                    push(@functionContent, "    $exceptionInit\n");
                    push(@functionContent, "    if ($content)\n");
                    push(@functionContent, "        return $toReturn;\n");
                    push(@functionContent, "    $exceptionRaiseOnError\n");
                    push(@functionContent, "    return $className();\n");
                } else {
                    push(@functionContent, "    if ($content)\n");
                    push(@functionContent, "        return $toReturn;\n");
                    push(@functionContent, "    return NULL;\n");
                }
            } else {
                if (ConversionNeeded($function->signature->type)) {
                    $content = "toWebKit(WTF::getPtr($content))";
                }

                if ($raisesExceptions) {
                    # Differentiated between when the return type is a pointer and
                    # not for white space issue (ie. Foo *result vs. int result).
                    if ($returnType =~ /\*$/) {
                        $content = $returnType . "result = " . $content;
                    } else {
                        $content = $returnType . " result = " . $content;
                    }

                    push(@functionContent, "    $exceptionInit\n");
                    push(@functionContent, "    $content;\n");
                    push(@functionContent, "    $exceptionRaiseOnError\n");
                    push(@functionContent, "    return result;\n");
                } else {
                    push(@functionContent, "    return $content;\n");
                }
            }

            my $conditionalString = GenerateConditionalString($function->signature);
            push(@implContent, "\n#if ${conditionalString}\n") if $conditionalString;

            push(@implContent, "$functionSig\n");
            push(@implContent, "{\n");
            push(@implContent, AddEarlyReturnStatement($returnType));
            push(@implContent, @functionContent);
            push(@implContent, "}\n\n");

            push(@implContent, "#endif\n\n") if $conditionalString;

            # Clear the hash
            %needsCustom = ();
        }
    }

    # END implementation

    # Generate internal interfaces
    my $namespace = GetNamespaceForClass($implClassName);
    push(@implContent, "$namespace" . "::$implClassName* toWebCore(const $className& wrapper)\n");
    push(@implContent, "{\n");
    push(@implContent, "    return wrapper.impl();\n");
    push(@implContent, "}\n\n");

    push(@implContent, "$className toWebKit($namespace" . "::$implClassName* value)\n");
    push(@implContent, "{\n");
    push(@implContent, "    return $className(value);\n");
    push(@implContent, "}\n");

    # - End the ifdef conditional if necessary
    push(@implContent, "\n#endif // ${conditionalString}\n") if $conditionalString;
}

# Internal helper
sub WriteData
{
    my $object = shift;
    my $name = shift;

    # Open files for writing...
    my $headerFileName = "$outputDir/" . $name . ".h";
    my $implFileName = "$outputDir/" . $name . ".cpp";

    # Remove old files.
    unlink($headerFileName);
    unlink($implFileName);

    # Write public header.
    open(HEADER, ">$headerFileName") or die "Couldn't open file $headerFileName";
    
    print HEADER @headerContentHeader;
    print HEADER "\n";
    foreach my $class (sort keys(%headerForwardDeclarations)) {
        if ($class =~ /::/) {
            my $namespacePart = $class;
            $namespacePart =~ s/::.*//;

            my $classPart = $class;
            $classPart =~ s/${namespacePart}:://;

            print HEADER "namespace $namespacePart {\nclass $classPart;\n};\n\n";
        } else {
            print HEADER "class $class;\n"
        }
    }

    my $hasForwardDeclarations = keys(%headerForwardDeclarations);
    print HEADER "\n" if $hasForwardDeclarations;
    print HEADER @headerContent;
    close(HEADER);

    @headerContentHeader = ();
    @headerContent = ();
    %headerForwardDeclarations = ();

    # Write implementation file.
    open(IMPL, ">$implFileName") or die "Couldn't open file $implFileName";

    print IMPL @implContentHeader;

    foreach my $include (sort keys(%implIncludes)) {
        # "className.h" is already included right after config.h, silence check-webkit-style
        next if $include eq "$name.h";
        print IMPL "#include \"$include\"\n";
    }

    print IMPL @implContent;
    close(IMPL);

    @implContentHeader = ();
    @implContent = ();
    %implIncludes = ();
}

1;
