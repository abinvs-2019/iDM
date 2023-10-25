import os
import requests

def download_file(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def download_ts_video(manifest_url, output_filename):
    # Download the manifest file
    download_file(manifest_url, 'manifest.m3u8')
    
    # Parse the manifest file to get the TS segment URLs
    with open('manifest.m3u8') as f:
        lines = f.readlines()
        ts_urls = [line.strip() for line in lines if line.startswith('http')]
    
    # Create a list to store the video binary data
    video_data = []
    
    # Download the TS segments
    for i, ts_url in enumerate(ts_urls):
        download_file(ts_url, f'segment_{i}.ts')
        with open(f'segment_{i}.ts', 'rb') as segment_file:
            video_data.append(segment_file.read())
        os.remove(f'segment_{i}.ts')
    
    # Combine the binary data into a single video
    with open(output_filename, 'wb') as out_file:
        for data in video_data:
            out_file.write(data)
    
    # Clean up temporary files
    os.remove('manifest.m3u8')

if __name__ == "__main__":
    manifest_url = 'https://streamcdneu.loco.gg/LVQYC9RP2M_fd6371f6-9f8f-4435-9631-a86aeca860cf/LVQYC9RP2M_fd6371f6-9f8f-4435-9631-a86aeca860cf_low/manifest.m3u8'
    output_filename = 'eagle_output.mp4'
    download_ts_video(manifest_url, output_filename)
