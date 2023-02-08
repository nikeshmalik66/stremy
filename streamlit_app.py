import openai
import streamlit as st
import sqlite3
from PIL import Image
import time

openai.api_key = "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"

# Database Connection
col1, col2 = st.columns(2)
conn = sqlite3.connect('bank.db')
c = conn.cursor()

def chatbot():
   
    st.title("Welcome to OneInsurance")

    policy_doc_link = "https://www.hdfcergo.com/docs/default-source/downloads/policy-wordings/health/arogya-sanjeevani---a5-size---pw---hehi.pdf"
    
    with col1:
        
        question_1 = "Do you want health insurance?"
        options_1 = ["Yes", "No"]

        st.write(question_1)
        selected_option_1 = st.selectbox("Please enter your option:", options_1)
        if selected_option_1 == "No":
            st.write("Thank you")
            image = Image.open('D:\alegria\one insurance\source\assets\img\thank you.jpg')
            st.image(image, caption='Please visit again!')
            return

        question_2 = "Select the Institution from where you want the Insurance"
        options_2 = ["Select something","Bank of Baroda", "State Bank of India(SBI)", "HDFC Bank", "LIC"]

        st.subheader(question_2)
        selected_option_2 = st.selectbox("Please enter your option:", options_2)

    with col2:
        if selected_option_2 == "Bank of Baroda":
            st.image('https://1000logos.net/wp-content/uploads/2021/06/Bank-of-Baroda-logo.png')
        elif selected_option_2 == "State Bank of India(SBI)":
            st.image('https://1000logos.net/wp-content/uploads/2018/03/SBI-Logo.png')
        elif selected_option_2 == "HDFC Bank":
            st.image('https://1000logos.net/wp-content/uploads/2021/06/HDFC-Bank-logo.png')
        elif selected_option_2 == "LIC":
            st.image('https://1000logos.net/wp-content/uploads/2021/08/LIC-Logo.png')

        # Get comprehensive information about the selected bank
        comprehensive_info = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Please provide comprehensive information about {selected_option_2}",
            max_tokens=250,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text
        st.write("Comprehensive information:")
        st.write(comprehensive_info)

    with col1:
        c.execute('SELECT Policy_Name FROM BANK WHERE Bank_Name= "{}"'.format(selected_option_2))
        options_3 = c.fetchall()

        # st.write(options_3)
        my_options = []
        for row in options_3:
            my_options.append(row[0])

        st.subheader("Select the Policy Name")
        selected_option_3 = st.selectbox("Please enter your option:", my_options)
    with col2:
        c.execute('SELECT Policy_doc FROM BANK WHERE Policy_Name = "{}"'.format(selected_option_3))
        policy_doc_link = c.fetchone()
        # Get comprehensive information about the selected bank
        info = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Please provide comprehensive information about {selected_option_3}",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text
        st.write("Information:")
        st.write(info)
    with col1:
        st.write("Loading...")
        # Add loading animation
        bar = st.progress(0)
        for i in range(100):
            # Update the progress bar with each iteration
            bar.progress(i + 1)
        time.sleep(0.05)
    
        st.write("")  # add a newline after the loading bar
        if selected_option_3 != None:
            st.subheader("List of Questions")            
            question_list= """ 

                    1. What is covered under the policy?
                    2. What are the policy exclusions?
                    3. What are the conditions to avail the benefits of the insurance policy?
                    4. What is the policy deductible and how does it work?
                    5. What is the policy's out-of-pocket maximum?
                    6. What is the policy's co-pay amount?
                    7. Is there a network of providers or can I see any doctor I choose?
                    8. Are pre-existing conditions covered under the policy?
                    9. What is the process for filing a claim?
                    10. What is the policy's premium and how often is it due?
                    11. How does the policy handle cost-sharing for prescription drugs?
                    12. Are there any limits on the number of visits or treatments for a particular condition?
                    13. Does the policy offer coverage for mental health services and rehabilitation? 
                    """

            st.write(question_list)
            def switch_question(argument):
                switch = {
                            1: "What is covered under the policy?",
                            2: "What are the policy exclusions?",
                            3: "What are the conditions to avail the benefits of the insurance policy?",
                            4: "What is the policy deductible and how does it work?",
                            5: "What is the policy's out-of-pocket maximum?",
                            6: "What is the policy's co-pay amount?",
                            7: "Is there a network of providers or can I see any doctor I choose?",
                            8: "Are pre-existing conditions covered under the policy?",
                            9: "What is the process for filing a claim?",
                            10: "What is the policy's premium and how often is it due?",
                            11: "How does the policy handle cost-sharing for prescription drugs?",
                            12: "Are there any limits on the number of visits or treatments for a particular condition?",
                            13: "Does the policy offer coverage for mental health services and rehabilitation?"
                    }
                return switch.get(argument, "Invalid Input")

            question_number = st.number_input("Please select a question number", min_value=1, max_value=13)
            selected_question = switch_question(question_number)
            response = "Sorry, I cannot answer that."

            if selected_question != "Invalid Input":
                response = openai.Completion.create(
                            model="text-davinci-003",
                            prompt="Read the following PDF Document\n\n{}\n\nAnswer the question based on the document provided\n{}".format(policy_doc_link, selected_question),
                            temperature=0,
                            max_tokens=250,
                            top_p=1,
                            frequency_penalty=0.5,
                            presence_penalty=0,
                            stop=["?"]
                )


                message = response.choices[0].text
                st.write(f"Answer: {message}")
            else:
                st.write(response)
    with col2:
        def fetch_data():
        # connect to the database
            conn1 = sqlite3.connect("life_insurer_data.db")

        # create a cursor
            cursor = conn1.cursor()

        # fetch the data from the database
            fetch_query = """
            SELECT * FROM life_insurer_data;
            """
            cursor.execute(fetch_query)
            data = cursor.fetchall()

        # close the connection to the database
            conn.close()

            return data

    # display the data in a table
        st.title("Life Insurer Data")
        st.write("Data Scrapped from https://freefincal.com/irda-life-insurance-claim-settlement-ratio-2023/")
        st.write("Data fetched from SQLite database")

        life_insurers = [row[0] for row in fetch_data()]
        selected_life_insurer = st.selectbox("Select a life insurer", life_insurers)

        with st.spinner("Fetching data..."):
            time.sleep(2)
            for row in fetch_data():
                if row[0] == selected_life_insurer:
                    st.write(f"Claim Settlement Ratio for {row[0]}: {row[1]}")

if __name__ == '__main__':
    chatbot()