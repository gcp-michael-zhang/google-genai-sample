import time
from google import genai
from google.genai import types

# VEO_MODEL_ID = "veo-3.0-generate-001"
# VEO_MODEL_ID = "veo-3.0-fast-generate-001"
# VEO_MODEL_ID = "veo-3.0-generate-preview"
VEO_MODEL_ID = "veo-3.0-fast-generate-preview"

client = genai.Client(
    vertexai=True,
    project="zhmichael-demo",
    location="us-central1",
)

prompt = "a close-up shot of a golden retriever playing in a field of sunflowers" # @param {type: "string"}

# Optional parameters
negative_prompt = "barking, woofing" # @param {type: "string"}
aspect_ratio = "16:9" # @param ["16:9","9:16"]
resolution = "1080p" # @param ["720p","1080p"]
enhance_prompt = True  # @param {type: 'boolean'}
generate_audio = True  # @param {type: 'boolean'}
starting_image = "./1.jpg"
output_gcs = "gs://zhmichael-test/Veo"


operation = client.models.generate_videos(
    model=VEO_MODEL_ID,
    prompt=prompt,
    # image=types.Image.from_file(location=starting_image), #图生视频，如果需要图生视频可以指定文件路径并且取消#
    config=types.GenerateVideosConfig(
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        number_of_videos=2, # 1 video generated per request
        duration_seconds=6,
        person_generation="allow_all",
        enhance_prompt=enhance_prompt,
        generate_audio=generate_audio,
        negative_prompt=negative_prompt,
        # output_gcs_uri=output_gcs,
    ),
)

# Waiting for the video(s) to be generated
while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)
    print(operation)

print(operation.result.generated_videos)

for n, generated_video in enumerate(operation.result.generated_videos):
    generated_video.video.save(f'video{n}.mp4') # Saves the video(s), 如果指定了gcs uri，这个调用会失败， NotImplementedError: Saving remote videos is not supported.