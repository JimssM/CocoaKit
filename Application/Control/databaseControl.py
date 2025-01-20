#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3

from Application.Model.model import gl_info
from Application.public import database_path


def update_database():
    """
    Updates the database with the provided data, inserting new entries or updating existing ones based on unique constraints.
    """
    # Connect to the database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Keys corresponding to the database columns
    keys = ["data1", "data2"]

    # Collect data from global information
    data_list = []
    data_list.append(gl_info.data1)
    data_list.append(gl_info.data2)

    # Log data to the server (commented out here)
    data = {
        keys[0]: gl_info.data1,
        keys[1]: gl_info.data2,
    }
    # log_to_server(data)

    # Prepare valid keys, values, and placeholders for the SQL query
    valid_keys = []
    valid_values = []
    placeholders = []

    for key, value in zip(keys, data_list):
        if value != "-1":  # Only include valid data
            valid_keys.append(key)
            valid_values.append(value)
            placeholders.append('?')

    # Convert lists to strings for the SQL query
    keys_str = ', '.join(valid_keys)
    placeholders_str = ', '.join(placeholders)

    # Generate the UPSERT SQL statement
    update_str = ', '.join([f"{key}=excluded.{key}" for key in valid_keys if key not in ['username', 'server']])
    sql = f'''
        INSERT INTO acc_state ({keys_str}) VALUES ({placeholders_str})
        ON CONFLICT(username, server) DO UPDATE SET {update_str}
        '''
    # Execute the SQL query for insertion or update
    try:
        cursor.execute(sql, valid_values)
        conn.commit()
        print("Data inserted or updated successfully.")
    except sqlite3.IntegrityError as e:
        print("Data insertion or update failed:", e)
    except sqlite3.OperationalError as e:
        print("SQL query error:", e)
    finally:
        # Close the database connection
        conn.close()
