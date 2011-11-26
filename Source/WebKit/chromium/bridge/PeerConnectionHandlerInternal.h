/*
 * Copyright (C) 2011 Google Inc. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1.  Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 * 2.  Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY APPLE INC. AND ITS CONTRIBUTORS ``AS IS'' AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL APPLE INC. OR ITS CONTRIBUTORS BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef PeerConnectionHandlerInternal_h
#define PeerConnectionHandlerInternal_h

#if ENABLE(MEDIA_STREAM)

#include "MediaStreamDescriptor.h"
#include "WebPeerConnectionHandlerClient.h"
#include <wtf/OwnPtr.h>
#include <wtf/PassRefPtr.h>
#include <wtf/text/WTFString.h>

namespace WebKit {
class WebPeerConnectionHandler;
class WebString;
class WebMediaStreamDescriptor;
}

namespace WebCore {

class PeerConnectionHandlerClient;
class SecurityOrigin;

class PeerConnectionHandlerInternal : public WebKit::WebPeerConnectionHandlerClient {
public:
    PeerConnectionHandlerInternal(PeerConnectionHandlerClient*, const String& serverConfiguration, PassRefPtr<SecurityOrigin>);
    ~PeerConnectionHandlerInternal();

    virtual void produceInitialOffer(const MediaStreamDescriptorVector& pendingAddStreams);
    virtual void handleInitialOffer(const String& sdp);
    virtual void processSDP(const String& sdp);
    virtual void processPendingStreams(const MediaStreamDescriptorVector& pendingAddStreams, const MediaStreamDescriptorVector& pendingRemoveStreams);
    virtual void sendDataStreamMessage(const char* data, size_t length);
    virtual void stop();

    // WebKit::WebPeerConnectionHandlerClient implementation.
    virtual void didCompleteICEProcessing();
    virtual void didGenerateSDP(const WebKit::WebString& sdp);
    virtual void didReceiveDataStreamMessage(const char* data, size_t length);
    virtual void didAddRemoteStream(const WebKit::WebMediaStreamDescriptor&);
    virtual void didRemoveRemoteStream(const WebKit::WebMediaStreamDescriptor&);

private:
    OwnPtr<WebKit::WebPeerConnectionHandler> m_webHandler;
    PeerConnectionHandlerClient* m_client;
};

} // namespace WebCore

#endif // ENABLE(MEDIA_STREAM)

#endif // PeerConnectionHandlerInternal_h
