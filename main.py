import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium  # برای ادغام folium با streamlit
from datetime import datetime

# اضافه کردن استایل CSS برای تغییر پس‌زمینه و فونت‌ها
st.markdown(
    """
    <style>
    body {
        background-color: #F0F8FF;  /* رنگ پس‌زمینه آبی روشن */
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3 {
        color: #FF6347; /* تغییر رنگ تیترها به نارنجی مایل به قرمز */
    }
    .css-145kmo2 {
        background-color: #FFFFFF; /* تغییر رنگ پس‌زمینه جعبه‌های نمایش به سفید */
        border-radius: 10px; /* افزودن انحنای لبه‌ها */
        padding: 15px;  /* افزایش فضای داخلی */
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);  /* افزودن سایه ملایم */
    }
    </style>
    """, unsafe_allow_html=True
)

# اضافه کردن لوگو در بالای صفحه با حاشیه‌ها و وسط‌چین کردن
st.markdown("""
    <div style="text-align: center;">
        <img src="https://img.icons8.com/?size=100&id=BsPifv14cJQt&format=png&color=000000/icons8-motorcycle-delivery-single-box-64.png" width="120">
    </div>
    """, unsafe_allow_html=True)

# عنوان اصلی داشبورد
st.markdown("<h1 style='text-align: center;'>داشبورد سفارش غذای روزانه</h1>", unsafe_allow_html=True)

# داده‌های ساختگی برای نمونه
data = {
    'order_id': [1, 2, 3, 4, 5],
    'customer_id': [101, 102, 103, 104, 105],
    'restaurant_name': ['Restaurant A', 'Restaurant B', 'Restaurant C', 'Restaurant D', 'Restaurant E'],
    'order_time': ['2024-10-05 12:00:00', '2024-10-05 13:30:00', '2024-10-05 14:00:00', '2024-10-05 15:00:00', '2024-10-05 17:00:00'],
    'delivery_time': ['2024-10-05 12:30:00', '2024-10-05 14:00:00', '2024-10-05 14:40:00', '2024-10-05 15:45:00', '2024-10-05 17:30:00'],
    'delivery_duration': [30, 30, 40, 45, 30],
    'rating': [4.5, 4.0, 5.0, 3.5, 4.5],
    'restaurant_latitude': [35.6895, 35.7005, 35.6910, 35.6980, 35.6800],
    'restaurant_longitude': [51.3890, 51.4000, 51.3915, 51.3985, 51.3800],
    'delivery_location': ['Location 1', 'Location 2', 'Location 3', 'Location 4', 'Location 5']
}

# ایجاد دیتافریم با داده‌های نمونه
df = pd.DataFrame(data)

# تبدیل ستون‌های زمانی به datetime
df['order_time'] = pd.to_datetime(df['order_time'])
df['delivery_time'] = pd.to_datetime(df['delivery_time'])

# انتخاب تاریخ مورد نظر برای فیلتر داده‌ها
selected_date = st.date_input("تاریخ سفارش را انتخاب کنید:", datetime.now().date())

# فیلتر کردن داده‌ها بر اساس تاریخ انتخاب شده
filtered_df = df[df['order_time'].dt.date == pd.to_datetime(selected_date).date()]

# نمایش جدول سفارش‌ها با استایل زیبا
st.markdown(f"<h2 style='color: #2B7A78;'>سفارش‌های ثبت شده در تاریخ {selected_date}</h2>", unsafe_allow_html=True)
st.dataframe(filtered_df)

# نمایش تعداد سفارش‌های ثبت شده با استایل
st.markdown(f"<p style='font-size: 18px; color: #1E90FF;'>تعداد سفارش‌های ثبت شده: <strong>{filtered_df.shape[0]}</strong></p>", unsafe_allow_html=True)

# نمودار تعداد سفارش‌ها در ساعت‌های مختلف
st.markdown("<h3 style='color: #3A506B;'>توزیع تعداد سفارش‌ها براساس زمان ثبت سفارش</h3>", unsafe_allow_html=True)
filtered_df['hour'] = filtered_df['order_time'].dt.hour
plt.figure(figsize=(10, 6))
sns.countplot(x='hour', data=filtered_df, palette='coolwarm')
plt.xlabel('Order Registration Time')
plt.ylabel('Number Of Orders')
plt.title('Distribution Of Orders At Different Hours Of The Day', color='#3A506B')
st.pyplot(plt)

# نمودار رتبه‌بندی رستوران‌ها
st.markdown("<h3 style='color: #3A506B;'>رتبه‌بندی رستوران‌ها</h3>", unsafe_allow_html=True)
plt.figure(figsize=(10, 6))
sns.barplot(x='restaurant_name', y='rating', data=filtered_df, palette='viridis')
plt.xlabel('Restaurant Name')
plt.ylabel('Ranking')
plt.title('Ranking Of Restaurants In Registered Orders.', color='#3A506B')
st.pyplot(plt)

# نمودار خطی برای نمایش مدت زمان تحویل بر اساس رستوران‌ها
st.markdown("<h3 style='color: #3A506B;'>مدت زمان تحویل بر اساس رستوران‌ها</h3>", unsafe_allow_html=True)
plt.figure(figsize=(10, 6))
sns.lineplot(x='restaurant_name', y='delivery_duration', data=filtered_df, marker='o', color='b')
plt.xlabel('Restaurant Name')
plt.ylabel('Duration Of Delivery (Minutes)')
plt.title('Duration Of Delivery Based On Restaurants', color='#3A506B')
st.pyplot(plt)

# نمودار دایره‌ای برای درصد سفارش‌ها بر اساس رستوران‌ها
st.markdown("<h3 style='color: #3A506B;'>نمودار دایره‌ای تعداد سفارش‌ها بر اساس رستوران‌ها</h3>", unsafe_allow_html=True)
order_counts = filtered_df['restaurant_name'].value_counts()
plt.figure(figsize=(7, 7))
plt.pie(order_counts, labels=order_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3'))
plt.title('Percentage Of Orders Based On Restaurants', color='#3A506B')
st.pyplot(plt)

# نمودار جعبه‌ای (Boxplot) برای نمایش توزیع زمان تحویل بر اساس رستوران‌ها
st.markdown("<h3 style='color: #3A506B;'>نمودار جعبه‌ای مدت زمان تحویل بر اساس رستوران‌ها</h3>", unsafe_allow_html=True)
plt.figure(figsize=(10, 6))
sns.boxplot(x='restaurant_name', y='delivery_duration', data=filtered_df, palette='coolwarm')
plt.xlabel('Restaurant Name')
plt.ylabel('Duration Of Delivery (Minutes)')
plt.title('Delivery Time Distribution Based On Restaurants', color='#3A506B')
st.pyplot(plt)

# نمایش مکان‌های رستوران‌ها
st.markdown("<h3 style='color: #3A506B;'>مکان‌های رستوران‌ها</h3>", unsafe_allow_html=True)
restaurants = {
    'restaurant_name': ['Restaurant A', 'Restaurant B', 'Restaurant C', 'Restaurant D', 'Restaurant E'],
    'latitude': [35.6895, 35.7005, 35.6910, 35.6980, 35.6800],
    'longitude': [51.3890, 51.4000, 51.3915, 51.3985, 51.3800]
}

map_center = [restaurants['latitude'][0], restaurants['longitude'][0]]
m = folium.Map(location=map_center, zoom_start=12)

# افزودن رستوران‌ها به نقشه
for i in range(len(restaurants['restaurant_name'])):
    folium.Marker(
        location=[restaurants['latitude'][i], restaurants['longitude'][i]],
        popup=restaurants['restaurant_name'][i],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# نمایش نقشه در streamlit
st_folium(m, width=700, height=500)

# محاسبه و نمایش میانگین مدت زمان تحویل
avg_delivery_time = filtered_df['delivery_duration'].mean()
st.write(f"<p style='font-size: 18px;'>میانگین مدت زمان تحویل: <strong>{avg_delivery_time}</strong> دقیقه</p>", unsafe_allow_html=True)

# تجزیه و تحلیل بیشترین زمان سفارش
if not filtered_df.empty:
    most_order_time = filtered_df['hour'].mode()[0]
    st.write(f"<p style='font-size: 18px;'>پرتکرارترین زمان سفارش: <strong>ساعت {most_order_time}:00</strong></p>", unsafe_allow_html=True)
else:
    st.write("هیچ سفارشی در تاریخ انتخاب شده وجود ندارد.")