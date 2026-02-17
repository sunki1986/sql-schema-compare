import os
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# -----------------------------------
# Load environment variables
# -----------------------------------
load_dotenv()

SOURCE_SERVER = os.getenv("SOURCE_SERVER")
SOURCE_DB = os.getenv("SOURCE_DB")
SOURCE_USER = os.getenv("SOURCE_USER")
SOURCE_PWD = os.getenv("SOURCE_PWD")

TARGET_SERVER = os.getenv("TARGET_SERVER")
TARGET_DB = os.getenv("TARGET_DB")
TARGET_USER = os.getenv("TARGET_USER")
TARGET_PWD = os.getenv("TARGET_PWD")

# -----------------------------------
# Load config
# -----------------------------------
with open("config/config.json", "r") as f:
    config = json.load(f)

disable_config = config.get("disable", {})
schemas = config.get("schemas", [])

# -----------------------------------
# Paths
# -----------------------------------
BASE_DIR = Path(__file__).parent
DACPAC_DIR = BASE_DIR.parent / "output_dacpacs"
SQL_DIR = BASE_DIR.parent / "output_sql"
DACPAC_DIR.mkdir(exist_ok=True)
SQL_DIR.mkdir(exist_ok=True)

DACPAC_PATH = DACPAC_DIR / "source.dacpac"
OUTPUT_SQL = SQL_DIR / "sqlpackage_output.sql"

# -----------------------------------
# Helper: Build object filter
# -----------------------------------
def build_exclude_arguments():
    # Build a comma-separated list of object types to exclude based on the
    # `disable` config (flags set to true mean that object type should be
    # excluded).
    excluded = [obj_type for obj_type, disabled in disable_config.items() if disabled]

    if not excluded:
        return []

    # sqlpackage accepts a comma-separated value for ExcludeObjectTypes.
    return [f"/p:ExcludeObjectTypes={','.join(excluded)}"]

# Note: sqlpackage does not support schema filtering for Extract or Script actions as of Feb 2026.
# Any attempt to use /p:ExtractSchemas, /p:ScriptSchemas, or /p:IncludeSchemas will result in an error.

# -----------------------------------
# Step 1: Extract DACPAC from Source
# -----------------------------------
def extract_dacpac():
    print("🔹 Extracting DACPAC from source...")

    cmd = [
        "sqlpackage",
        "/Action:Extract",
        f"/SourceServerName:{SOURCE_SERVER}",
        f"/SourceDatabaseName:{SOURCE_DB}",
        f"/SourceUser:{SOURCE_USER}",
        f"/SourcePassword:{SOURCE_PWD}",
        "/SourceTrustServerCertificate:True",
        f"/TargetFile:{DACPAC_PATH}"
    ]

    # Only exclusions for extract step
    cmd.extend(build_exclude_arguments())

    subprocess.run(cmd, check=True)
    print("✅ DACPAC created.")


# -----------------------------------
# Step 2: Generate Deploy Script
# -----------------------------------
def generate_diff_script():
    print("🔹 Generating schema comparison script...")

    cmd = [
        "sqlpackage",
        "/Action:Script",
        f"/SourceFile:{DACPAC_PATH}",
        f"/TargetServerName:{TARGET_SERVER}",
        f"/TargetDatabaseName:{TARGET_DB}",
        f"/TargetUser:{TARGET_USER}",
        f"/TargetPassword:{TARGET_PWD}",
        "/SourceTrustServerCertificate:True",
        "/TargetTrustServerCertificate:True",
        f"/OutputPath:{OUTPUT_SQL}"
    ]

    cmd.extend(build_exclude_arguments())

    subprocess.run(cmd, check=True)
    print(f"✅ Deployment script generated at {OUTPUT_SQL}")

# -----------------------------------
# Step 3: Deploy Script to Target
# -----------------------------------
def deploy_script():
    print("🔹 Deploying script to target...")

    cmd = [
        "sqlcmd",
        "-S", TARGET_SERVER,
        "-U", TARGET_USER,
        "-P", TARGET_PWD,
        "-C",
        "-d", TARGET_DB,
        "-i", str(OUTPUT_SQL)
    ]

    subprocess.run(cmd, check=True)
    print("✅ Deployment completed.")
# -----------------------------------
# Main
# -----------------------------------
if __name__ == "__main__":
    try:
        extract_dacpac()
        generate_diff_script()
        print("🎯 Schema comparison completed successfully.")
        #deploy script basis user input yes or not
        user_input = input("Do you want to deploy the script? (yes/no): ")
        if user_input.lower() == "yes":
            deploy_script()

    except subprocess.CalledProcessError as e:
        print("❌ Error during execution:", e)
