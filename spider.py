import requests
import os
import yt_dlp
from dotenv import load_dotenv

load_dotenv()

authorization_token = os.getenv("AUTHORIZATION")

headers = {
    "authorization": f"Bearer {authorization_token}",
    "origin": "https://blackbankers.app.cativa.digital",
    "plah-customer": "cpaclub",
    "referer": "https://blackbankers.app.cativa.digital/",
}


base_url = "https://social-api.cativalab.digital/v1.1/course/6d6b4a6f-f786-4cbb-6437-08dc6f6f8048"


def scrape():
    response = requests.get(
        url=f"{base_url}/preview",
        headers=headers,
    ).json()

    course_name = response["name"]
    module_id = 0
    for module in response["modules"]:
        module_name = module["name"]

        lesson_id = 0
        for lesson in module["lessons"]:
            video_id = lesson["id"]
            attachments = get_attachments_data(video_id)
            module_formated_title = f"{module_id}  {module_name.replace('/', '_')}"
            lesson_formated_title = (
                f"{lesson_id}  {attachments['lesson_title'].replace('/', '_')}"
            )
            path = os.path.join(
                course_name, module_formated_title, lesson_formated_title
            )
            os.makedirs(path, exist_ok=True)

            if pdf := attachments["attachments"]:
                pdf_name_formated = pdf[0]["file_name"].replace("/", "_")
                with open(f"{path}/{pdf_name_formated}.pdf", "wb") as f:
                    f.write(requests.get(pdf[0]["file_url"]).content)

            if video := attachments["videos"]:
                yt_dlp_opts = {
                    "format": "worst",
                    "outtmpl": f"{path}/%(title)s.%(ext)s",
                }
                try:
                    with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
                        ydl.download([video])
                except Exception as e:
                    print(f"Error downloading video: {e}")

            lesson_id += 1
        module_id += 1


def get_attachments_data(video_id):
    video_api_url = f"{base_url}/lesson/{video_id}"

    response = requests.get(
        url=video_api_url,
        headers=headers,
    ).json()["post"]

    attachments = [
        {
            "file_name": attach.get("filename"),
            "file_url": attach.get("url"),
        }
        for attach in response.get("attachments")
    ]

    videos = response["linkAttachment"]["url"] if response.get("linkAttachment") else ""

    lesson_title = response["title"]

    return {
        "videos": videos,
        "attachments": attachments,
        "lesson_title": lesson_title,
    }


if __name__ == "__main__":
    scrape()
