from google_auth_oauthlib.flow import InstalledAppFlow

# YouTube Upload Scope
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    # Google Cloud se download ki gayi client_secret.json file ka path dein
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES
    )
    creds = flow.run_local_server(port=0)
    print("\n--- AAPKA REFRESH TOKEN ---")
    print(creds.refresh_token)

if __name__ == '__main__':
    main()
