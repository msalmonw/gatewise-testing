from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import boto3

def get_hls_url(stream_name):
    client = boto3.client('kinesisvideo')

    try:
        response = client.get_data_endpoint(
            StreamName=stream_name,
            APIName='GET_HLS_STREAMING_SESSION_URL')
        
        kvam_client = boto3.client("kinesis-video-archived-media", endpoint_url=response['DataEndpoint'])
        url = kvam_client.get_hls_streaming_session_url(
        StreamName='gatewise-camera-01',
        PlaybackMode="LIVE"
        )['HLSStreamingSessionURL']
        return url
    except Exception as e:
        return None


def kvs(request):
    url = get_hls_url('gatewise-camera-01')
    if url:
        context = {
            'hls_url': url
        }
    else:
        context = {
            'error_message': 'Live stream is not available at the moment.'
            }

    return render(request, 'kvs_stream/stream_template.html', context)
