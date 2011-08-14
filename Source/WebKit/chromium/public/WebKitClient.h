/*
 * Copyright (C) 2010 Google Inc. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *
 *     * Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above
 * copyright notice, this list of conditions and the following disclaimer
 * in the documentation and/or other materials provided with the
 * distribution.
 *     * Neither the name of Google Inc. nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef WebKitClient_h
#define WebKitClient_h

#include "WebAudioBus.h"
#include "WebAudioDevice.h"
#include "WebCommon.h"
#include "WebData.h"
#include "WebLocalizedString.h"
#include "WebSerializedScriptValue.h"
#include "WebString.h"
#include "WebVector.h"
#include "WebURL.h"

#include <time.h>

#ifdef WIN32
typedef void *HANDLE;
#endif

// FIXME: remove after rolling deps
#define WEBKIT_USE_MONOTONIC_CLOCK_FOR_TIMER_SCHEDULING

namespace WebKit {

class WebApplicationCacheHost;
class WebApplicationCacheHostClient;
class WebBlobRegistry;
class WebClipboard;
class WebCookieJar;
class WebFileSystem;
class WebFileUtilities;
class WebGraphicsContext3D;
class WebIDBFactory;
class WebIDBKey;
class WebMessagePortChannel;
class WebMimeRegistry;
class WebPluginListBuilder;
class WebSandboxSupport;
class WebSharedWorkerRepository;
class WebSocketStreamHandle;
class WebStorageNamespace;
class WebThemeEngine;
class WebThread;
class WebURLLoader;

class WebKitClient {
public:
    // Must return non-null.
    virtual WebClipboard* clipboard() { return 0; }

    // Must return non-null.
    virtual WebMimeRegistry* mimeRegistry() { return 0; }

    // Must return non-null.
    virtual WebFileUtilities* fileUtilities() { return 0; }

    // May return null if sandbox support is not necessary
    virtual WebSandboxSupport* sandboxSupport() { return 0; }

    // May return null on some platforms.
    virtual WebThemeEngine* themeEngine() { return 0; }

    // May return null.
    virtual WebCookieJar* cookieJar() { return 0; }

    // Blob ----------------------------------------------------------------

    // Must return non-null.
    virtual WebBlobRegistry* blobRegistry() { return 0; }

    // DOM Storage --------------------------------------------------

    // Return a LocalStorage namespace that corresponds to the following path.
    virtual WebStorageNamespace* createLocalStorageNamespace(const WebString& path, unsigned quota) { return 0; }

    // Called when storage events fire.
    virtual void dispatchStorageEvent(const WebString& key, const WebString& oldValue,
                                      const WebString& newValue, const WebString& origin,
                                      const WebURL& url, bool isLocalStorage) { }


    // History -------------------------------------------------------------

    // Returns the hash for the given canonicalized URL for use in visited
    // link coloring.
    virtual unsigned long long visitedLinkHash(
        const char* canonicalURL, size_t length) { return 0; }

    // Returns whether the given link hash is in the user's history.  The
    // hash must have been generated by calling VisitedLinkHash().
    virtual bool isLinkVisited(unsigned long long linkHash) { return false; }


    // HTML5 Database ------------------------------------------------------

#ifdef WIN32
    typedef HANDLE FileHandle;
#else
    typedef int FileHandle;
#endif

    // Opens a database file; dirHandle should be 0 if the caller does not need
    // a handle to the directory containing this file
    virtual FileHandle databaseOpenFile(
        const WebString& vfsFileName, int desiredFlags) { return FileHandle(); }

    // Deletes a database file and returns the error code
    virtual int databaseDeleteFile(const WebString& vfsFileName, bool syncDir) { return 0; }

    // Returns the attributes of the given database file
    virtual long databaseGetFileAttributes(const WebString& vfsFileName) { return 0; }

    // Returns the size of the given database file
    virtual long long databaseGetFileSize(const WebString& vfsFileName) { return 0; }

    // Returns the space available for the given origin
    virtual long long databaseGetSpaceAvailableForOrigin(const WebKit::WebString& originIdentifier) { return 0; }

    // Indexed Database ----------------------------------------------------

    virtual WebIDBFactory* idbFactory() { return 0; }
    virtual void createIDBKeysFromSerializedValuesAndKeyPath(const WebVector<WebSerializedScriptValue>& values,  const WebString& keyPath, WebVector<WebIDBKey>& keys) { }
    virtual WebSerializedScriptValue injectIDBKeyIntoSerializedValue(const WebIDBKey& key, const WebSerializedScriptValue& value, const WebString& keyPath) { return WebSerializedScriptValue(); }


    // Keygen --------------------------------------------------------------

    // Handle the <keygen> tag for generating client certificates
    // Returns a base64 encoded signed copy of a public key from a newly
    // generated key pair and the supplied challenge string. keySizeindex
    // specifies the strength of the key.
    virtual WebString signedPublicKeyAndChallengeString(unsigned keySizeIndex,
                                                        const WebKit::WebString& challenge,
                                                        const WebKit::WebURL& url) { return WebString(); }



    // Memory --------------------------------------------------------------

    // Returns the current space allocated for the pagefile, in MB.
    // That is committed size for Windows and virtual memory size for POSIX
    virtual size_t memoryUsageMB() { return 0; }

    // Same as above, but always returns actual value, without any caches.
    virtual size_t actualMemoryUsageMB() { return 0; }


    // Threads -------------------------------------------------------

    // Creates an embedder-defined thread.
    virtual WebThread* createThread(const char* name) { return 0; }


    // Message Ports -------------------------------------------------------

    // Creates a Message Port Channel.  This can be called on any thread.
    // The returned object should only be used on the thread it was created on.
    virtual WebMessagePortChannel* createMessagePortChannel() { return 0; }


    // Network -------------------------------------------------------------

    // A suggestion to prefetch IP information for the given hostname.
    virtual void prefetchHostName(const WebString&) { }

    // Returns a new WebURLLoader instance.
    virtual WebURLLoader* createURLLoader() { return 0; }

    // Returns a new WebSocketStreamHandle instance.
    virtual WebSocketStreamHandle* createSocketStreamHandle() { return 0; }

    // Returns the User-Agent string that should be used for the given URL.
    virtual WebString userAgent(const WebURL&) { return WebString(); }

    // A suggestion to cache this metadata in association with this URL.
    virtual void cacheMetadata(const WebURL&, double responseTime, const char* data, size_t dataSize) { }


    // Plugins -------------------------------------------------------------

    // If refresh is true, then cached information should not be used to
    // satisfy this call.
    virtual void getPluginList(bool refresh, WebPluginListBuilder*) { }


    // Profiling -----------------------------------------------------------

    virtual void decrementStatsCounter(const char* name) { }
    virtual void incrementStatsCounter(const char* name) { }

    // An event is identified by the pair (name, id).  The extra parameter
    // specifies additional data to log with the event.
    virtual void traceEventBegin(const char* name, void* id, const char* extra) { }
    virtual void traceEventEnd(const char* name, void* id, const char* extra) { }

    // Callbacks for reporting histogram data.
    // CustomCounts histogram has exponential bucket sizes, so that min=1, max=1000000, bucketCount=50 would do.
    virtual void histogramCustomCounts(const char* name, int sample, int min, int max, int bucketCount) { }
    // Enumeration histogram buckets are linear, boundaryValue should be larger than any possible sample value.
    virtual void histogramEnumeration(const char* name, int sample, int boundaryValue) { }


    // Resources -----------------------------------------------------------

    // Returns a blob of data corresponding to the named resource.
    virtual WebData loadResource(const char* name) { return WebData(); }

    // Decodes the in-memory audio file data and returns the linear PCM audio data in the destinationBus.
    // A sample-rate conversion to sampleRate will occur if the file data is at a different sample-rate.
    // Returns true on success.
    virtual bool loadAudioResource(WebAudioBus* destinationBus, const char* audioFileData, size_t dataSize, double sampleRate) { return false; }

    // Returns a localized string resource (with substitution parameters).
    virtual WebString queryLocalizedString(WebLocalizedString::Name) { return WebString(); }
    virtual WebString queryLocalizedString(WebLocalizedString::Name, const WebString& parameter) { return WebString(); }
    virtual WebString queryLocalizedString(WebLocalizedString::Name, const WebString& parameter1, const WebString& parameter2) { return WebString(); }


    // Sandbox ------------------------------------------------------------

    // In some browsers, a "sandbox" restricts what operations a program
    // is allowed to preform.  Such operations are typically abstracted out
    // via this API, but sometimes (like in HTML 5 database opening) WebKit
    // needs to behave differently based on whether it's restricted or not.
    // In these cases (and these cases only) you can call this function.
    // It's OK for this value to be conservitive (i.e. true even if the
    // sandbox isn't active).
    virtual bool sandboxEnabled() { return false; }


    // Shared Workers ------------------------------------------------------

    virtual WebSharedWorkerRepository* sharedWorkerRepository() { return 0; }

    // Sudden Termination --------------------------------------------------

    // Disable/Enable sudden termination.
    virtual void suddenTerminationChanged(bool enabled) { }


    // System --------------------------------------------------------------

    // Returns a value such as "en-US".
    virtual WebString defaultLocale() { return WebString(); }

    // Wall clock time in seconds since the epoch.
    virtual double currentTime() { return 0; }

    // Monotonically increasing time in seconds from an arbitrary fixed point in the past.
    // This function is expected to return at least millisecond-precision values. For this reason,
    // it is recommended that the fixed point be no further in the past than the epoch.
    virtual double monotonicallyIncreasingTime() { return 0; }

    // WebKit clients must implement this funcion if they use cryptographic randomness.
    virtual void cryptographicallyRandomValues(unsigned char* buffer, size_t length) = 0;

    // Delayed work is driven by a shared timer.
    typedef void (*SharedTimerFunction)();
    virtual void setSharedTimerFiredFunction(SharedTimerFunction timerFunction) { }
    virtual void setSharedTimerFireInterval(double) { }
    virtual void stopSharedTimer() { }

    // Callable from a background WebKit thread.
    virtual void callOnMainThread(void (*func)(void*), void* context) { }

    // WebGL --------------------------------------------------------------

    // May return null if WebGL is not supported.
    // Returns newly allocated WebGraphicsContext3D instance.
    virtual WebGraphicsContext3D* createGraphicsContext3D() { return 0; }

    // Audio --------------------------------------------------------------

    virtual double audioHardwareSampleRate() { return 0; }
    virtual WebAudioDevice* createAudioDevice(size_t bufferSize, unsigned numberOfChannels, double sampleRate, WebAudioDevice::RenderCallback*) { return 0; }

    // FileSystem ----------------------------------------------------------

    // Must return non-null.
    virtual WebFileSystem* fileSystem() { return 0; }

protected:
    ~WebKitClient() { }
};

} // namespace WebKit

#endif
