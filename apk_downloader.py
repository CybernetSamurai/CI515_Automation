import time
from playwright.sync_api import sync_playwright

def download_apk(package_name, download_folder="downloads"):
    apkcombo_url = f"https://apkcombo.com/en/{package_name}/download/apk"

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print(f"[+] Navigating to {apkcombo_url}")
        page.goto(apkcombo_url)

        # Wait for the download button to be available
        page.wait_for_selector("a.button.is-success")

        # Start the download
        with page.expect_download() as download_info:
            page.click("a.button.is-success")
        download = download_info.value

        # Save the file
        apk_path = download.save_as(f"{download_folder}/{package_name}.apk")
        print(f"[+] APK downloaded to {apk_path}")

        browser.close()


if __name__ == "__main__":
    # Example package - replace with any package name you want to test
    package = "com.starbucks.mobilecard"
    download_apk(package)
