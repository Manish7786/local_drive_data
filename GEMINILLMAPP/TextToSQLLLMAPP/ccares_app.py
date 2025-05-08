from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import psycopg2
import google.generativeai as genai

## Configure API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini model and provide sql query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

## Function to retrieve query from the PostgreSQL database
def read_sql_query(sql):
    try:
        conn = psycopg2.connect(
            dbname="ccares",
            user="postgres",
            password="onlyshouvikknowsthepassword",
            host="10.180.146.63",
            port="27018"
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        return [("Error", str(e))]

## Define Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!\n
    If query did not give any data then simply give response as (I don't know).\n
    The SQL database has the name ccares and has the table name - member_details, t_pf_claim, t_pf_claim_track, family_member.\n
    Table member_details has following columns -"member_id" (PRIMARY KEY),"cmpf_acc_no","title_id","full_name","father_hus_name","gender",
    "marital_status","religion_id","date_of_birth","address_l1","address_l2","land_no","email","aadhaar_id","pf_nominee_decl",
    "pension_nominee_decl","pan_id","verify_status","verify_date","enrol_req_id","nom_vrfy_status","nom_verify_remarks",
    "employee_id","joining_date","pf_start_date","pf_end_date","bank_acc_no_pf","ifsc_pf","bank_acc_no_pen","ifsc_pen",
    "fath_hus_flag","mobile_no","village","city","district","pincode","country","unit_id","state","consent_status","bank_id_pf",
    "bank_id_pen","pen_nom_share","pension_nominee","pf_nom_share","pf_nominee","new_mem_status","emp_type"\n
    Table t_pf_claim has following columns - "pf_claim_srno" (PRIMARY KEY),"claim_id","member_id","uda_login_id","name_aadhaar","name_pan",
    "name_bank","nm_aadhaar_match","nm_pan_match","nm_bank_match","dob_aadhaar","dob_pan","sfwh_name","sfwh_relation_type",
    "pf_claim_typ_id","declaration_uda","aao_confrm_payment","date_received","pf_claim_status_id","roda_login_id","claimant_id",
    "total_disbursed_perctg","settlement_date","ledger_balance","claimed_amount","date_of_cessation","sanctioned_amt","pay_order",
    "pay_order_no","date_of_death","dpo_date","po_dated","process_id","draft_pay_order"\n
    Table t_pf_claim_track has following columns - "pf_activity_track_id","pf_claim_srno","pf_claim_status_id","remarks",
    "status","activity_date","from_offcr_login_id","to_offcr_login_id"\n
    Table family_member has following columns - "family_mem_id","member_id","verified_status","title_id","name","fath_hus_name",
    "relation_id","gender","marital_status","religion_id","date_of_birth","address_l1","address_l2","mobile_no","land_no","email_id",
    "fam_mem_state","district","pincode","pan_id","fam_mem_status","pf_nominee","pension_nominee","pf_nom_share_perc",
    "pen_nom_share_perc","fam_aadhaar_id","village","city","country","bank_acc_no","bank_id"
    \n\n For Example,
    \nExample 1 - How many entries of records are present?,
    the SQL command will be something like this SELECT COUNT(*) FROM member_details;
    \nExample 2 - Tell me name of member with cmpf no RMG/2/311?,
    the SQL command will be something like this SELECT full_name FROM member_details WHERE cmpf_acc_no='RMG/2/311';
    \nExample 3 - How many total members are there?,
    the SQL command will be something like this SELECT count(DISTINCT member_id) FROM member_details;
    \nExample 4 - Give me the name of member id 80499?,
    the SQL command will be something like this SELECT full_name FROM member_details WHERE member_id = 80499;
    \nExample 5 - My claim with cmpf acc number HYD/52/2478 is at which officer?,
    the SQL command will be something like this SELECT to_offcr_login_id FROM t_pf_claim_track JOIN t_pf_claim ON t_pf_claim.pf_claim_srno = t_pf_claim_track.pf_claim_srno JOIN member_details ON t_pf_claim.member_id = member_details.member_id WHERE cmpf_acc_no = 'HYD/52/2478' ORDER BY pf_activity_track_id DESC LIMIT 1;
    \nExample 6 - What is the latest remark on my claim with cmpf account number HYD/52/2478?,
    the SQL command will be something like this SELECT remarks FROM t_pf_claim_track JOIN t_pf_claim ON t_pf_claim.pf_claim_srno = t_pf_claim_track.pf_claim_srno JOIN member_details ON t_pf_claim.member_id = member_details.member_id WHERE cmpf_acc_no = 'HYD/52/2478' ORDER BY pf_activity_track_id DESC LIMIT 1;
    \nExample 7 - What date the claim has submitted for cmpf no HYD/52/2478?,
    the SQL command will be something like this SELECT date_received FROM t_pf_claim JOIN member_details ON member_details.member_id = t_pf_claim.member_id WHERE cmpf_acc_no = 'HYD/52/2478';
    \nExample 8 - Who is the nominee of cmpf acc no RNJ/17/2062?,
    the SQL command will be something like this SELECT name FROM family_member JOIN member_details ON member_details.member_id = family_member.member_id WHERE (family_member.pf_nominee = TRUE OR family_member.pension_nominee = TRUE) AND cmpf_acc_no = 'RNJ/17/2062';
    \n Example 9 - What is the address of member with cmpf acc RNJ/17/2062?,
    the SQL command will be something like this SELECT address_l1, address_l2, village, city, district, state, pincode, country FROM member_details WHERE cmpf_acc_no = 'RNJ/17/2062';
    also the sql code should not have ``` in beginning or end and sql word in the output
    \n\nNote: If the user asks a question that is not related to the provided tables (member_details, t_pf_claim, t_pf_claim_track, family_member) or cannot be answered using this database, reply with:
    'This question is not related to the database and cannot be converted into an SQL query.'
    Do not attempt to generate SQL for such questions.

    """
]

## Streamlit app

st.set_page_config(page_title="C-Cares")
st.header("APP to Retrieve SQL Data from C-CARES Member details")

question = st.text_input("Input: ",key="input")

submit = st.button("Ask the question")

## If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    data = read_sql_query(response)
    st.subheader("The Response is")
    for row in data:
        print(row)
        st.header(row)

