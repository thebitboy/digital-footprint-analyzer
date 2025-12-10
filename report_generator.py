import pandas as pd

def generate_report(data, filename="privacy_report.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename
