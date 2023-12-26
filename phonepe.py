#Packages

import json
import streamlit as st
import pandas as pd
import requests
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from PIL import Image

#CREATE DATAFRAMES FROM SQL

#sql connection
mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        password = "anu123",
                        database = "phonepe_data",
                        port = "5432"
                        )
cursor = mydb.cursor()


#Aggregated_transsaction

cursor.execute("select * from aggregated_transaction")
mydb.commit()
table1 = cursor.fetchall()
Aggre_trans = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


#Aggregated_user
cursor.execute("select * from aggregated_user")
mydb.commit()
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_transaction
cursor.execute("select * from map_transaction")
mydb.commit()
table3 = cursor.fetchall()
Map_trans = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_user
cursor.execute("select * from map_user")
mydb.commit()
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))


#Top_transaction
cursor.execute("select * from top_transaction")
mydb.commit()
table5 = cursor.fetchall()
Top_trans = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


#Top_user
cursor.execute("select * from top_user")
mydb.commit()
table6 = cursor.fetchall()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))


def animate_all_amount():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1 = json.loads(response.content)
    
    frames = []

    attype= Aggre_trans[["States","Transaction_amount"]]
    att1= attype.groupby("States")["Transaction_amount"].sum()
    merged_df= pd.DataFrame(att1).reset_index()

    #merged_df = pd.concat(frames)
    merged_df["States"] = merged_df["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    merged_df["States"] = merged_df["States"].str.replace("-"," ")
    merged_df["States"] = merged_df["States"].str.title()
    merged_df['States'] = merged_df['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
    
    fig_tra = px.choropleth(merged_df, geojson= data1, 
                            locations= "States", featureidkey= "properties.ST_NM", color= "Transaction_amount",
                            color_continuous_scale= "Sunsetdark", range_color= (0,4000000000),
                            hover_name= "States", title = "TRANSACTION AMOUNT", scope="asia"
                           )
    #animation_frame="Years", animation_group="Quarter",

    fig_tra.update_geos(fitbounds= "locations", visible =False)
    fig_tra.update_layout(width =600, height= 700,title_font= {"size":25})
    return st.plotly_chart(fig_tra)
    
    
def payment_count():
    attype= Aggre_trans[["Transaction_type", "Transaction_count"]]
    att1= attype.groupby("Transaction_type")["Transaction_count"].sum()
    df_att1= pd.DataFrame(att1).reset_index()
    fig_pc= px.bar(df_att1,x= "Transaction_type",y= "Transaction_count",title="TRANSACTION TYPE AND TRANSACTION COUNT",
                color_discrete_sequence=px.colors.sequential.Redor_r)
    fig_pc.update_layout(width=600, height= 500)
    return st.plotly_chart(fig_pc)

def animate_all_count():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tra= [feature["properties"]["ST_NM"]for feature in data1["features"]]
    state_names_tra.sort()

    df_state_names_tra= pd.DataFrame({"States":state_names_tra})

    frames= []
  
    attype= Aggre_trans[["States","Transaction_count"]]
    att1= attype.groupby("States")["Transaction_count"].sum()
    merged_dff= pd.DataFrame(att1).reset_index()
 
    #merged_ff = pd.concat(frames)
    #merged_dff= merged_ff.groupby("States")["Transaction_count"].sum()
    merged_dff["States"] = merged_dff["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    merged_dff["States"] = merged_dff["States"].str.replace("-"," ")
    merged_dff["States"] = merged_dff["States"].str.title()
    merged_dff['States'] = merged_dff['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
 
    fig_tra= px.choropleth(merged_dff, geojson= data1, locations= "States",featureidkey= "properties.ST_NM",
                        color= "Transaction_count",color_continuous_scale= 'Reds', 
                        title="TRANSACTION COUNT", hover_name= "States")
    #animation_frame="Years", animation_group= "Quarter"

    fig_tra.update_geos(fitbounds= "locations", visible= False)
    fig_tra.update_layout(width= 600, height= 700,title_font={"size":25})  
    return st.plotly_chart(fig_tra)


def payment_amount():
    attype= Aggre_trans[["Transaction_type","Transaction_amount"]]
    att1= attype.groupby("Transaction_type")["Transaction_amount"].sum()
    df_att1= pd.DataFrame(att1).reset_index()
    fig_tra_pa= px.bar(df_att1, x= "Transaction_type", y= "Transaction_amount", title= "TRANSACTION TYPE AND TRANSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Blues_r)
    fig_tra_pa.update_layout(width= 600, height= 500)
    return st.plotly_chart(fig_tra_pa)

def reg_all_states(state):
    mu= Map_user[["States","Districts","RegisteredUser"]]
    mu1= mu.loc[(mu["States"]==state)]
    mu2=mu1[["Districts", "RegisteredUser"]]
    mu3= mu2.groupby("Districts")["RegisteredUser"].sum()
    mu4= pd.DataFrame(mu3).reset_index()
    
    fig_mu= px.bar(mu4, x= "Districts", y= "RegisteredUser", title= "DISTRICTS AND REGISTERED USER",
                    color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_mu.update_layout(width= 1000, height= 500)
    return st.plotly_chart(fig_mu)

def transaction_amount_year(sel_year):
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tra= [feature["properties"]['ST_NM']for feature in data1["features"]]
    state_names_tra.sort()

    year= int(sel_year)
    atay= Aggre_trans[["States","Years","Transaction_amount"]]
    atay1= atay.loc[(Aggre_trans["Years"]==year)]
    atay2= atay1.groupby("States")["Transaction_amount"].sum()
    atay3= pd.DataFrame(atay2).reset_index()

    atay3["States"] = atay3["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    atay3["States"] = atay3["States"].str.replace("-"," ")
    atay3["States"] = atay3["States"].str.title()
    atay3['States'] = atay3['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    fig_atay= px.choropleth(atay3, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                            color= "Transaction_amount", color_continuous_scale="rainbow", range_color=(0,800000000000),
                            title="TRANSACTION AMOUNT AND STATES", hover_name= "States")

    fig_atay.update_geos(fitbounds= "locations", visible= False)
    fig_atay.update_layout(width=600,height=700)
    fig_atay.update_layout(title_font= {"size":25})
    return st.plotly_chart(fig_atay)         


def payment_count_year(sel_year):
    year= int(sel_year)
    apc= Aggre_trans[["Transaction_type", "Years", "Transaction_count"]]
    apc1= apc.loc[(Aggre_trans["Years"]==year)]
    apc2= apc1.groupby("Transaction_type")["Transaction_count"].sum()
    apc3= pd.DataFrame(apc2).reset_index()

    fig_apc= px.bar(apc3,x= "Transaction_type", y= "Transaction_count", title= "PAYMENT COUNT AND PAYMENT TYPE",
                    color_discrete_sequence=px.colors.sequential.Brwnyl_r)
    fig_apc.update_layout(width=600, height=500)
    return st.plotly_chart(fig_apc)

def transaction_count_year(sel_year):
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1=json.loads(response.content)
    state_names_tra= [feature["properties"]["ST_NM"]for feature in data1["features"]]
    state_names_tra.sort()

    year= int(sel_year)
    atcy= Aggre_trans[["States", "Years", "Transaction_count"]]
    atcy1= atcy.loc[(Aggre_trans["Years"]==year)]
    atcy2= atcy1.groupby("States")["Transaction_count"].sum()
    atcy3= pd.DataFrame(atcy2).reset_index()

    atcy3["States"] = atcy3["States"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    atcy3["States"] = atcy3["States"].str.replace("-"," ")
    atcy3["States"] = atcy3["States"].str.title()
    atcy3['States'] = atcy3['States'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    fig_atcy= px.choropleth(atcy3, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                            color= "Transaction_count", color_continuous_scale= "rainbow",range_color=(0,3000000000),
                            title= "TRANSACTION COUNT AND STATES",hover_name= "States")
    fig_atcy.update_geos(fitbounds= "locations", visible= False)
    fig_atcy.update_layout(width=600, height= 700)
    fig_atcy.update_layout(title_font={"size":25})
    return st.plotly_chart(fig_atcy)


def payment_amount_year(sel_year):
    year= int(sel_year)
    apay = Aggre_trans[["Years", "Transaction_type", "Transaction_amount"]]
    apay1= apay.loc[(Aggre_trans["Years"]==year)]
    apay2= apay1.groupby("Transaction_type")["Transaction_amount"].sum()
    apay3= pd.DataFrame(apay2).reset_index()

    fig_apay= px.bar(apay3, x="Transaction_type", y= "Transaction_amount", title= "PAYMENT TYPE AND PAYMENT AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Burg_r)
    fig_apay.update_layout(width=600, height=500)
    return st.plotly_chart(fig_apay)


def reg_state_all_RU(sel_year,state):
    year= int(sel_year)
    mus= Map_user[["States", "Years", "Districts", "RegisteredUser"]]
    mus1= mus.loc[(Map_user["States"]==state)&(Map_user["Years"]==year)]
    mus2= mus1.groupby("Districts")["RegisteredUser"].sum()
    mus3= pd.DataFrame(mus2).reset_index()

    fig_mus= px.bar(mus3, x= "Districts", y="RegisteredUser", title="DISTRICTS AND REGISTERED USER",
                    color_discrete_sequence=px.colors.sequential.Cividis_r)
    fig_mus.update_layout(width= 600, height= 500)
    return st.plotly_chart(fig_mus)

def reg_state_all_TA(sel_year,state):
    year= int(sel_year)
    mts= Map_trans[["States", "Years","Districts", "Transaction_amount"]]
    mts1= mts.loc[(Map_trans["States"]==state)&(Map_trans["Years"]==year)]
    mts2= mts1.groupby("Districts")["Transaction_amount"].sum()
    mts3= pd.DataFrame(mts2).reset_index()

    fig_mts= px.bar(mts3, x= "Districts", y= "Transaction_amount", title= "DISTRICT AND TRANSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Darkmint_r)
    fig_mts.update_layout(width= 600, height= 500)
    return st.plotly_chart(fig_mts)

def ques1():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggre_trans[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)


def ques3():
    htd= Map_trans[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= Map_trans[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)

def ques5():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_trans[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_trans[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_st= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_st)


def ques9():
    ht= Aggre_trans[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index()
    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)


def ques10():
    dt= Map_trans[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)


    
st.set_page_config(layout= "wide")

st.title(":violet[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]")

tab1, tab2, tab3 = st.tabs(["***HOME***","***EXPLORE DATA***","***TOP CHARTS***"])


with tab1:
    col1,col2= st.columns(2)

    with col1:
        st.header(":violet[PHONEPE]")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown(" :violet[Phonepe is an Indian digital payments and financial technology company]")
        st.write("****FEATURES****")
        st.write("   **-> :violet[Credit & Debit card linking]**")
        st.write("   **-> :violet[CBank Balance check]**")
        st.write("   **-> :violet[CMoney Storage]**")
        st.write("   **-> :violet[CPIN Authorization]**")
        
        image=Image.open('C:/Users/vinoth/Desktop/New folder/Phonepe/phonepe_660_050221042103.webp')
        st.image(image,width=200)
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("C:/Users/vinoth/Desktop/New folder/Phonepe/pulse-video.mp4") 

    col3,col4= st.columns(2)
    
    with col3:
        
        st.video("C:/Users/vinoth/Desktop/New folder/Phonepe/home-fast-secure-v3.mp4") 
                        
    with col4:

        st.write("**-> :violet[Easy Transactions]**")
        st.write("**-> :violet[One App For All Your Payments]**")
        st.write("**-> :violet[Your Bank Account Is All You Need]**")
        st.write("**-> :violet[Multiple Payment Modes]**")
        st.write("**-> :violet[PhonePe Merchants]**")
        st.write("**-> :violet[Multiple Ways To Pay]**")
        st.write("**-  :violet[1.Direct Transfer & More]**")
        st.write("**-  :violet[2.QR Code]**")
        st.write("**-> :violet[Earn Great Rewards]**")
        image=Image.open('C:/Users/vinoth/Desktop/New folder/Phonepe/Pulse-Insight-Header-Pulse-Bytes-Size.webp')
        st.image(image,width=200)

    col5,col6= st.columns(2)
    

    with col5:

        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("**-> :violet[No Wallet Top-Up Required]**")
        st.write("**-> :violet[Pay Directly From Any Bank To Any Bank A/C]**")
        st.write("**-> :violet[Instantly & Free]**")

        image=Image.open('C:/Users/vinoth/Desktop/New folder/Phonepe/phonepe.gif')
        st.image(image,width=200)
    with col6:
        
        video_url = "https://youtu.be/aXnNA4mv1dU?si=WYA0iMunvWvwxS4j"
        st.video(video_url)
        

with tab2:
    
    
    sel_year = st.selectbox(":violet[Select the Year]",("All", "2018", "2019", "2020", "2021", "2022", "2023"))
    if sel_year == "All" :
        col1, col2 = st.columns(2)
        
        with col1:         
            animate_all_count()     
            payment_count()
        
        with col2:
            animate_all_amount()
            payment_amount()        
       
        state=st.selectbox(":violet[Select the state]",('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                'dadra-&-nagar-&-haveli-&-daman-&-diu','delhi','goa',
                                                'gujarat','haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                                                'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                                                'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                                'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                                                'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                'uttarakhand', 'west-bengal'))
        reg_all_states(state)
        
    else:
        col1,col2= st.columns(2)

        with col1:
            
            transaction_count_year(sel_year)
            payment_count_year(sel_year)

        with col2:
              
            transaction_amount_year(sel_year)
            
            payment_amount_year(sel_year)
            state= st.selectbox(":violet[Select the state]",('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                'dadra-&-Nagar-&-haveli-&-daman-&-diu','delhi','goa',
                                                'gujarat','haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                                                'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                                                'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                                'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                                                'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                'uttarakhand', 'west-bengal'))
            reg_state_all_RU(sel_year,state)
            reg_state_all_TA(sel_year,state)
           
            

with tab3:
    
    
    ques= st.selectbox(":violet[Select the question]",('Top Brands Of Mobiles Used','States With Lowest Transaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Transaction Count',
                                 'States With Highest Transaction Count','States With Highest Transaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))


    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Transaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Transaction Count":
        ques7()

    elif ques=="States With Highest Transaction Count":
        ques8()

    elif ques=="States With Highest Transaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()

   