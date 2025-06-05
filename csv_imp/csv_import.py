from db.graph_driver import neo4j_driver
import pandas as pd
from utils.uuid import get_uuid

excel_file = r"D:\Personal\CSV\new_persons.xlsx"
df = pd.read_excel(excel_file)

# Clean column names and drop unnamed columns
df.columns = df.columns.str.strip()
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# List of phone columns to clean
phone_cols = ['Phone_1', 'Phone_2', 'Phone_3', 'Phone_4']

# Format phones: convert to string with '+' and remove decimals
for col in phone_cols:
    df[col] = df[col].apply(lambda x: f"+{int(x)}" if pd.notna(x) and str(x).strip() != "" else "")

# Create 'person_phone' column as list of cleaned phones
df['person_phone'] = df[phone_cols].apply(
    lambda row: [phone for phone in row if phone and str(phone).strip() != ""],
    axis=1
)

# Rename 'Title' to 'person_name' for clarity
df.rename(columns={'Title': 'person_name'}, inplace=True)

# Select and reorder required columns
df_final = df[['person_name', 'person_phone', 'Org_1', 'Org_2', 'Country']]


# Add UUID column
df_final.loc[:, 'person_id']  = df_final.apply(lambda _: str(get_uuid()), axis=1)

# --- Neo4j Create Person Node ---
def create_person(tx, person_id, name, phones, org1, org2, country):
    tx.run("""
        MERGE (p:Person {person_id: $person_id})
        SET p.person_name = $name,
            p.person_phone = $phones,
            p.org1 = $org1,
            p.org2 = $org2,
            p.country = $country
    """, person_id=person_id, name=name, phones=phones, org1=org1, org2=org2, country=country)

# Insert into Neo4j
with neo4j_driver.get_driver().session() as session:
    for _, row in df_final.iterrows():
        session.execute_write(
            create_person,
            row['person_id'],
            row['person_name'],
            row['person_phone'],
            row.get('Org_1', ''),
            row.get('Org_2', ''),
            row.get('Country', '')
        )