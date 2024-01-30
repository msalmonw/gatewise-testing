import boto3
import numpy as np
import cv2

client = boto3.client('kinesisvideo')

response = client.get_data_endpoint(
        StreamName='gatewise-camera-01',
        APIName='GET_HLS_STREAMING_SESSION_URL')

kvam_client = boto3.client("kinesis-video-archived-media", endpoint_url=response['DataEndpoint'])
url = kvam_client.get_hls_streaming_session_url(
    StreamName='gatewise-camera-01',
    PlaybackMode="LIVE"
    )['HLSStreamingSessionURL']

capture = cv2.VideoCapture(url)

fps = capture.get(cv2.CAP_PROP_FPS)
wait_ms = int(1000/fps)
print('FPS:', fps)

while(True):
    # Capture frame-by-frame
    ret, frame = capture.read()

    if frame is not None:
        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Press q to close the video windows before it ends if you want
        if cv2.waitKey(wait_ms) & 0xFF == ord('q'):
            break
    else:
        print("Frame is None")
        break

# When everything done, release the capture
capture.release()
cv2.destroyAllWindows()
print("Video stop")