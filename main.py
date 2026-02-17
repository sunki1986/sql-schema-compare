from compare.sqlpackage import extract_dacpac, generate_diff_script, deploy_script

if __name__ == "__main__":
    try:
        extract_dacpac()
        generate_diff_script()
        print("🎯 Schema comparison completed successfully.")
        #deploy script basis user input yes or not
        user_input = input("Do you want to deploy the script? (yes/no): ")
        if user_input.lower() == "yes":
            deploy_script()

    except Exception as e:
        print("❌ Error during execution:", e)