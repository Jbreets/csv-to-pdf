import chardet
import pandas as pd

def filter_by_email(parq_file, email_csv):
    # Process the email CSV file
    email_content = email_csv.read()  # Read the file content as bytes
    email_csv.seek(0)  # Reset the file pointer to the beginning
    result = chardet.detect(email_content)  # Detect encoding
    encoding = result['encoding'] if result['encoding'] else 'utf-8'


    # Read the email CSV into a DataFrame
    emails = pd.read_csv(email_csv, encoding=encoding, header=None)
    emails = emails.dropna(how="all")  # Drop completely empty rows

    # Extract emails and convert to a set
    data_list = emails.iloc[:, 0].tolist()
    email_set = set(data_list)

    # Columns to keep in the final output
    columns_to_keep = [
        "First name", "Last name", "Date of birth", "Gender", "Event city",
        "Event date", "Weight", "Previous experience", "Medical details"
    ]

    # Process the parq file
    parq_content = parq_file.read()  # Read the file content as bytes
    parq_file.seek(0)  # Reset the file pointer to the beginning
    result = chardet.detect(parq_content)  # Detect encoding
    encoding = result['encoding']

    # Read the parq file into a DataFrame
    parq = pd.read_csv(parq_file, encoding=encoding)
    parq = parq.dropna(how="all")  # Drop completely empty rows

    # Format the "Date of birth" column
    parq['Date of birth'] = pd.to_datetime(parq['Date of birth'], errors='coerce').dt.strftime('%d/%m/%Y')

    # Filter the parq DataFrame based on the email set
    filtered_parq = parq[parq["Email"].isin(email_set)]
    filtered_parq = filtered_parq[columns_to_keep]

    # Save the filtered data to a new CSV file
    filtered_parq.to_csv("downloads/parq-cleaned-data.csv", index=False)


# Example usage
# email_names = {"rolandhegedus13@gmail.com", "stefaniuk1086@gmail.com", "reeceacleary@yahoo.co.uk", "jackflahavan11@gmail.com"}  # Define a proper set
# filtered_df = filter_by_email("test-parq-report.csv", email_names)
# filter_by_email("test-parq-report.csv", "test-emails.csv")


# print(filtered_df)