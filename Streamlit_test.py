import streamlit as st
import pandas as pd
from HypothesisTests import HypothesisTestInterface


st.title("Hypothesis Testing")

uploaded_file = st.file_uploader('upload')
if uploaded_file != None:
    df = pd.read_csv(uploaded_file)


    selection = st.sidebar.selectbox("Please select which test you want to go with :",["Tests","One sample tests","Two sample tests","More than two sample test"])
    htI = HypothesisTestInterface()

    if selection == 'One sample tests':
        test_inp = st.sidebar.selectbox("Please select which test you want to go with:",
                    ["1. One sample t test with 2 tails", 
                    "2. One sample z test with 2 tails",
                    "3. One sample t test with 1 tail lower",
                    "4. One sample z test with 1 tail lower",
                    "5. One sample t test with 1 tail upper",
                    "6. One sample z test with 1 tail upper"])
        
        
        if test_inp == "1. One sample t test with 2 tails":
            myTest = htI.select_test(samples="oneSample",test = "t", tails='twoTail',type=None)
            try: 
                cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            except:
                st.write("Please select the columns")
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    target_value = st.number_input("Please enter the Target mean value:")
                    alpha = st.number_input("Please enter the Alpha value:")
                    if st.button("Run Test"):
                        if myTest.run_test([cols], alpha,df, target_value):
                            st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                        else:
                            st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        elif test_inp == "2. One sample z test with 2 tails":
            myTest = htI.select_test(samples="oneSample",test = "z", tails='twoTail',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    target_value = st.number_input("Please enter the Target mean value:")
                    alpha = st.number_input("Please enter the Alpha  value:")
                    if st.button("Run Test"):
                        if myTest.run_test([cols], alpha,df, target_value):
                            st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                        else:
                            st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        elif test_inp == "3. One sample t test with 1 tail lower":
            myTest = htI.select_test(samples="oneSample",test = "t", tails='oneTailL',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    target_value = st.number_input("Please enter the Target mean value:")
                    alpha = st.number_input("Please enter the Alpha  value:")
                    if st.button("Run Test"):
                        if myTest.run_test([cols], alpha,df, target_value):
                            st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                        else:
                            st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        elif test_inp == "4. One sample z test with 1 tail lower":
            myTest = htI.select_test(samples="oneSample",test = "z", tails='oneTailL',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    target_value = st.number_input("Please enter the Target mean value:")
                    alpha = st.number_input("Please enter the Alpha  value:")
                    if st.button("Run Test"):
                        if myTest.run_test([cols], alpha,df, target_value):
                            st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                        else:
                            st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        elif test_inp == "5. One sample t test with 1 tail upper":
            myTest = htI.select_test(samples="oneSample",test = "t", tails='oneTailG',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    target_value = st.number_input("Please enter the Target mean value:")
                    alpha = st.number_input("Please enter the Alpha  value:")
                    if st.button("Run Test"):
                        if myTest.run_test([cols], alpha,df, target_value):
                            st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                        else:
                            st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        elif test_inp == "6. One sample z test with 1 tail upper":
            myTest = htI.select_test(samples="oneSample",test = "z", tails='oneTailG',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    target_value = st.number_input("Please enter the Target mean value:")
                    alpha = st.number_input("Please enter the Alpha  value:")
                    if st.button("Run Test"):
                        if myTest.run_test([cols], alpha,df, target_value):
                            st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                        else:
                            st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
    elif selection == 'Two sample tests':
        test_inp = st.sidebar.selectbox("Please select which test you want to go with:",
                   ["1. Two sample t test with 2 tails", 
                    "2. Two sample z test with 2 tails",
                    "3. Two sample t test with 1 tail lower",
                    "4. Two sample z test with 1 tail lower",
                    "5. Two sample t test with 1 tail upper",
                    "6. Two sample z test with 1 tail upper",
                    "7. Welch t test with 2 tails",
                    "8. Welch t test with 1 tail lower",
                    "9. Welch t test with 1 tail upper",
                    "10. Wilcoxan signed rank test with 2 tails",
                    "11. Wilcoxan signed rank test with 1 tail lower",
                    "12. Wilcoxan signed rank test with 1 tail upper",
                    "13. Mann Witney U test with 2 tails",
                    "14. Mann Witney U test with 1 tail lower",
                    "15. Mann Witney U test with 1 tail upper"
                    ])
        if test_inp == "1. Two sample t test with 2 tails":
            myTest = htI.select_test(samples='twoSample',test = 't', tails='twoTail',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:    
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                        alpha_val = st.number_input("Please enter the Alpha value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis") 
        elif test_inp == "2. Two sample z test with 2 tails":
                myTest = htI.select_test(samples="twoSample",test = "z", tails='twoTail',type=None)
                cols = st.selectbox('Select the columns:',[None]+list(df.columns))
                if df[cols].dtypes == "object":
                    st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
                else:
                    st.write("You Selected:" , cols)
                    if cols != None:
                        st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                        category = str(st.selectbox("Please select the column you want to compare with",[None]+list(df.columns)))
                        if category != None:
                            column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                            alpha_val = st.number_input("Please enter the Alpha  value:")
                            if st.button("Run Test"):
                                if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                    st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                                else:
                                    st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        elif test_inp == "3. Two sample t test with 1 tail lower":
            myTest = htI.select_test(samples="twoSample",test = "t", tails='oneTailL',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")

        elif test_inp == "4. Two sample z test with 1 tail lower":
            myTest = htI.select_test(samples="twoSample",test = "z", tails='oneTailL',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis") 

        elif test_inp == "5. Two sample t test with 1 tail upper":
            myTest = htI.select_test(samples="twoSample",test = "t", tails='oneTailG',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")  

        elif test_inp == "6. Two sample z test with 1 tail upper":
            myTest = htI.select_test(samples="twoSample",test = "z", tails='oneTailG',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")

        elif test_inp == "7. Welch t test with 2 tails":
            myTest = htI.select_test(samples="twoSample",test = "Welch t", tails='twoTail',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        elif test_inp == "8. Welch t test with 1 tail lower":
            myTest = htI.select_test(samples="twoSample",test = "Welch t", tails='oneTailL',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                    
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        
        elif test_inp == "9. Welch t test with 1 tail upper":
            myTest = htI.select_test(samples="twoSample",test = "Welch t", tails='oneTailG',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")

        elif test_inp == "10. Wilcoxan signed rank test with 2 tails":
            myTest = htI.select_test(samples="twoSample",test = "Wilcoxan", tails='twoTail',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                        
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        
        elif test_inp == "11. Wilcoxan signed rank test with 1 tail lower":
            myTest = htI.select_test(samples="twoSample",test = "Wilcoxan", tails='oneTailL',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                    
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        
        elif test_inp == "12. Wilcoxan signed rank test with 1 tail upper":
            myTest = htI.select_test(samples="twoSample",test = "Wilcoxan", tails='oneTailG',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                        
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        
        elif test_inp == "13. Mann Witney U test with 2 tails":
            myTest = htI.select_test(samples="twoSample",test = "Mann-Witney", tails='twoTail',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                        
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
            
        elif test_inp == "14. Mann Witney U test with 1 tail lower":
            myTest = htI.select_test(samples="twoSample",test = "Mann-Witney", tails='oneTailL',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        
        elif test_inp == "15. Mann Witney U test with 1 tail upper":
            myTest = htI.select_test(samples="twoSample",test = "Mann-Witney", tails='oneTailG',type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2 = st.multiselect('Select the columns:', df[category].unique())
                        alpha_val = st.number_input("Please enter the Alpha  value:")
                        if st.button("Run Test"):
                            if myTest.run_test([cols],category,column1,column2,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
        

    elif selection == "More than two sample test":
        test_inp = st.sidebar.selectbox("Please select which test you want to go with:",
                   ["1. Analysis of Variance(ANOVA)",
                    "2. Kruskal Wallis H Test",
                    "3. Moods Median Test"
                   ])

        if test_inp == "1. Analysis of Variance(ANOVA)":
            myTest1 = htI.select_test1(samples1 = "morethantwoSample",test1="anova",type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2,column3 = st.multiselect('Select the columns:', df[category].unique())
                        category1 = df[df[category] == column1]
                        category2 = df[df[category] == column2]
                        category3 = df[df[category] == column3]
                        alpha_val = st.number_input("Please enter the Alpha value:")
                        if st.button("Run Test"):
                            if myTest1.run_test1([cols],category1,category2,category3,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")

        elif test_inp == "2. Kruskal Wallis H Test":
            myTest1 = htI.select_test1(samples1 = "morethantwoSample",test1="kruskal",type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2,column3 = st.multiselect('Select the columns:', df[category].unique())
                        category1 = df[df[category] == column1]
                        category2 = df[df[category] == column2]
                        category3 = df[df[category] == column3]
                        alpha_val = st.number_input("Please enter the Alpha value:")
                        if st.button("Run Test"):
                            if myTest1.run_test1([cols],category1,category2,category3,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
    
        elif test_inp == "3. Moods Median Test":
            myTest1 = htI.select_test1(samples1 = "morethantwoSample",test1="moods",type=None)
            cols = st.selectbox('Select the columns:',[None]+list(df.columns))
            if df[cols].dtypes == "object":
                st.write("PLEASE SELECT A COLUMN WITH NUMERICAL VALUE.")
            else:
                st.write("You Selected:" , cols)
                if cols != None:
                    st.write("Sample mean of the column you selected is:",round(df[cols].mean(),2))
                    category = st.selectbox("Please select the column you want to compare with",[None]+list(df.columns))
                    if category != None:
                        column1,column2,column3 = st.multiselect('Select the columns:', df[category].unique())
                        category1 = df[df[category] == column1]
                        category2 = df[df[category] == column2]
                        category3 = df[df[category] == column3]
                        alpha_val = st.number_input("Please enter the Alpha value:")
                        if st.button("Run Test"):
                            if myTest1.run_test1([cols],category1,category2,category3,alpha_val,df):
                                st.write("As the P value is greater than the entered Alpha value, we ACCEPT the null hypothesis")
                            else:
                                st.write("As the P value is less than the entered Alpha value, we REJECT the null hypothesis")
    