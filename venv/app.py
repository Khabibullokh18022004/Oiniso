import streamlit as st
import pandas as pd
import matplotlib

matplotlib.use('agg')
import seaborn as sns


# Boradagi harajatlarni yuklash yoki yangi DataFrame yaratish
def load_expenses():
    try:
        expenses = pd.read_csv("expenses.csv",index_col=[0])
        expenses['Sana'] = pd.to_datetime(expenses['Sana'])
        expenses = expenses.sort_values(by='Sana').reset_index(drop=True)
    except FileNotFoundError:
        expenses = pd.DataFrame(columns=["Sana", "Toifasi", "Miqdori"])
    return expenses


# Harajatni DataFrame ga qo'shish
def add_expense(expenses, date, category, amount):
    new_expense = pd.DataFrame({"Sana": [date], "Toifasi": [category], "Miqdori": [amount]})
    expenses = pd.concat([expenses, new_expense], ignore_index=True)
    expenses.to_csv("expenses.csv", index=False)
    return expenses


# Harajatlarni DataFrame dan o'chirish
def delete_expense(expenses, indices):
    expenses = expenses.drop(indices, axis=0)
    expenses.to_csv("expenses.csv", index=False)
    return expenses


# Harajat hisobotini generatsiya qilish
def generate_expense_report(expenses, start_date, end_date, report_format):
    expenses["Sana"] = pd.to_datetime(expenses["Sana"])  # Convert "Sana" column to datetime
    filtered_expenses = expenses[
        (expenses["Sana"] >= pd.to_datetime(start_date)) & (expenses["Sana"] <= pd.to_datetime(end_date))
        ]
    if report_format == "CSV":
        report = filtered_expenses.to_csv(index=False)
    elif report_format == "PDF":
        # PDF kutubxonasidan foydalanib PDF hisoboti yaratish
        report = "PDF hisobot"  # PDF yaratish kodi uchun o'rnating
    else:
        # Show report graph
        show_report_graph(filtered_expenses)
        report = "Graph displayed"
    return report


# Harajatlarni DataFrame ni ko'rsatish
def show_expenses(expenses):
    st.subheader("Harajatlar")
    selected_indices = st.multiselect("Harajatni O'chirish", expenses.index)
    if st.button("Tanlangan Harajatlarni o'chiring"):
        if selected_indices:
            expenses = delete_expense(expenses, selected_indices)
            st.success("Tanlangan Harajatlarni o'chirildi!")
        else:
            st.warning("Iltimos, o'chirish uchun harajatlarni tanlang.")
    st.dataframe(expenses)
    st.subheader("Harajat hisobotini generatsiya qilish")
    start_date = st.date_input("Boshlang'ich sana")
    end_date = st.date_input("Oxirgi sana")
    report_format = st.selectbox("Hisobot Format", ["CSV", "PDF", "Graph"])
    if st.button("Hisobotni generatsiya qilish"):
        report = generate_expense_report(expenses, start_date, end_date, report_format)
        if report_format == "CSV":
            st.download_button("CSV ni yuklab olish", data=report, file_name="expense_report.csv")
        elif report_format == "PDF":
            # PDF hisobotni yaratib chiqish yoki yuklab olish
            st.write("PDF hisobotni yuklab oling")
        else:
            st.write(report)


# Funksiya bo'limi hisobot uchun umumiy statistikalar chiqarish
def show_user_statistics(expenses):
    st.subheader("Foydalanuvchi Statistikasi")

    # Grafik 1: Kategoriya bo'yicha harajatlar
    st.subheader("Harajatlar Kategoriyalar Bo'yicha")
    expenses_by_category = expenses.groupby("Toifasi")["Miqdori"].sum()
    matplotlib.pyplot.figure(figsize=(10, 6))
    sns.barplot(x=expenses_by_category.index, y=expenses_by_category.values)
    matplotlib.pyplot.xticks(rotation=45)
    matplotlib.pyplot.xlabel("Kategoriya")
    matplotlib.pyplot.ylabel("Jami Miqdor")
    st.pyplot(matplotlib.pyplot)

    # Grafik 2: Oylik umumiy harajatlar
    st.subheader("Oylik Umumiy Harajatlar")
    expenses["Sana"] = pd.to_datetime(expenses["Sana"])
    expenses["Oy"] = expenses["Sana"].dt.strftime("%Y-%m")
    monthly_expenses = expenses.groupby("Oy")["Miqdori"].sum()
    matplotlib.pyplot.figure(figsize=(10, 6))
    matplotlib.pyplot.plot(monthly_expenses.index, monthly_expenses.values, marker='o')
    matplotlib.pyplot.xticks(rotation=45)
    matplotlib.pyplot.xlabel("Oy")
    matplotlib.pyplot.ylabel("Jami Miqdor")
    st.pyplot(matplotlib.pyplot)


# Funksiya hisobotni grafikini ko'rsatish
def show_report_graph(filtered_expenses):
    st.subheader("Harajatlar Hisoboti Grafiki")
    matplotlib.pyplot.figure(figsize=(10, 6))
    sns.histplot(filtered_expenses["Miqdori"], kde=True)
    matplotlib.pyplot.xlabel("Harajat Mikdori")
    matplotlib.pyplot.ylabel("Hisoblanadigan Harajatlar Soni")
    st.pyplot(matplotlib.pyplot)


# Asosiy funksiya
def main():
    st.title("Harajatlar Tracker")
    # Session holatini boshlash
    session_state = st.session_state.setdefault("session_state", {})

    # Yangi harajat qo'shish formasini ko'rsatish
    st.subheader("Yangi harajat qo'shish")
    date = st.date_input("Sana", value=pd.to_datetime("today"))
    category = st.text_input("Toifasi")
    amount = st.text_input("Miqdori", value="")

    # Harajatni qo'shish tugmasi
    if st.button("Saqlash"):
        session_state["expenses"] = add_expense(session_state["expenses"], date, category, amount)
        st.success("Harajat muvaffaqiyatli qo'shildi!")

    # Harajatlar yuklanmagan bo'lsa, yuklash
    if "expenses" not in session_state:
        session_state["expenses"] = load_expenses()

    # Harajatlarni ko'rsatish
    show_expenses(session_state["expenses"])

    # Foydalanuvchi statistikasini ko'rsatish
    show_user_statistics(session_state["expenses"])


# Dasturni boshlash
if __name__ == "__main__":
    main()
