import sqlite3
import pandas as pd

# Path to the copied chat.db
db_path = './chat.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)

# SQL Query
query = """
SELECT
    message.date / 1000000000 + 978307200 AS UnixEpoch,
    datetime(message.date / 1000000000 + 978307200, 'unixepoch', 'localtime') AS Date,
    message.text,
    CASE
        WHEN handle.id IS NULL OR handle.id = '' THEN 'Unknown'
        ELSE handle.id
    END AS Sender,
    chat.chat_identifier AS ChatID
FROM
    message
    JOIN chat_message_join ON message.ROWID = chat_message_join.message_id
    JOIN chat ON chat.ROWID = chat_message_join.chat_id
    LEFT JOIN handle ON message.handle_id = handle.ROWID
WHERE
    message.text IS NOT NULL
    AND message.text NOT LIKE 'Laughed at %'
    AND message.text NOT LIKE 'Liked %'
    AND message.text NOT LIKE 'Disliked %'
    AND message.text NOT LIKE 'Loved %'
    AND message.text NOT LIKE 'Questioned %'
    AND message.text NOT LIKE 'Emphasized %'
    AND DATE(datetime(message.date / 1000000000 + 978307200, 'unixepoch', 'localtime')) >= '2024-01-01'

ORDER BY
    message.date;
"""

# Execute the query and read into a pandas DataFrame
df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Debug print to see how many rows we got
print(f"Number of rows fetched: {len(df)}")

# Save to CSV only if there are rows fetched
if len(df) > 0:
    df.to_csv('iMessage_export.csv', index=False)
    print("CSV saved.")
    
    # Filter the DataFrame to keep only rows with 'Unknown' sender
    unknown_df = df[df['Sender'] == 'Unknown']
    
    # Save the filtered DataFrame to a new CSV file
    unknown_df.to_csv('iMessage_export_unknown.csv', index=False)
    print("CSV with unknown senders saved.")
else:
    print("No messages found matching the criteria.")
