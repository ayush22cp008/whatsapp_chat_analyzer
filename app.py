import streamlit as st
import preprocessor,helper
from helper import most_busy_user
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
upload_file=st.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preproces(data)
    st.title("Top Statistics")
    # fetch unique user
    user_list=df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)

    if st.sidebar.button("Analyze"):
        num_messages,words,num_media_messages,num_links= helper.fetch_stats(selected_user, df)
        col1,col2,col3,col4=st.columns(4)
        # total no of messages
        with col1:
           st.header("Total Messages")
           st.title(num_messages)
        # total no of Words
        with col2:
           st.header("Total Words")
           st.title(words)
        # total no of Media
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        # total no of Links
        with col4:
            st.header("Links Shared")
            st.title(num_links)

    # monthly timeline
    st.title("Monthly Timeline")
    timeline=helper.monthly_timeline(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(timeline['time'],timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # activity map
    st.title("Activity Map")
    col1, col2 = st.columns(2)
    with col1:
         st.header("Most Busy Day")
         busy_day=helper.weak_activity(selected_user,df)
         fig,ax=plt.subplots()
         ax.barh(busy_day.index,busy_day.values)
         plt.xticks(rotation='vertical')
         st.pyplot(fig)
    with col2:
        st.header("Most Busy Month")
        busy_month = helper.month_activity(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(busy_month.index, busy_month.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title("Weakly Activity Map")
    user_heatmap=helper.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax=sns.heatmap(user_heatmap)
    st.pyplot(fig)

    #find the busiest user in group chat
    if selected_user=="Overall":
        st.title("Most Busy User")
        x,y=helper.most_busy_user(df)
        fig,ax=plt.subplots()
        col1,col2 = st.columns(2)
        with col1:
             ax.bar(x.index,x.values)
             plt.xticks(rotation='vertical')
             st.pyplot(fig)
        with col2:
            st.dataframe(y)

    # wordcloud
    st.title("WordCloud")
    df_wc=helper.create_wordcloud(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    #most common words
    most_common_df=helper.most_common_words(selected_user,df)
    fig,ax=plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title("Most Common Words")
    st.pyplot(fig)

    # most common emojis
    emoji_df=helper.emoji(selected_user,df)
    st.title("Most Common Emojis")
    st.dataframe(emoji_df)






