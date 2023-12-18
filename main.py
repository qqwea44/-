import streamlit as st
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt


# Определение пола по умолчанию
if 'gender' not in st.session_state:
    st.session_state['gender'] = 'Юноши'
# Функция для предсказания оценок на основе нормативов
def predict_marks(df):
   # Загрузка нормативов из JSON файла
    json_file_path = "normatives.json"

    # Открытие файла JSON для чтения
    with open(json_file_path, "r", encoding="utf-8") as json_file:

        data = json.load(json_file)
    
    #print(data['Test'].keys())
    insertion_columns = []
    insertion_columns_names = []
    insertion_columns_types = []
    insertion_columns_source = []
    for k in range(len(df.keys())):
        #print(df.keys()[k])
        if df.keys()[k].split('.')[0] in data['Test'].keys():
            insertion_columns.append(k)
            insertion_columns_names.append(str(df.keys()[k]) + ' оценка')
            insertion_columns_types.append(str(df.keys()[k]).split('.')[0])
            insertion_columns_source.append(df.keys()[k])
            #df.insert(k, str(df.keys()[k]) + ' оценка' + str(k), np.zeros(len(df)))
            #print(k)
    # Обработка данных и предсказание оценок
    counter = 1
    for i in range(len(insertion_columns)):
        insertion = np.zeros(len(df))
        #print(data['Test'][insertion_columns_types[i]][st.session_state['gender']])
        for j in range(len(df)):
            try:
                value_orig = float(df[insertion_columns_source[i]][j])
                value = None
                bigger  = float(data['Test'][insertion_columns_types[i]][st.session_state['gender']]['5'])
                smaller  = float(data['Test'][insertion_columns_types[i]][st.session_state['gender']]['1'])
                if bigger > smaller:
                    for k in range(5, 1, -1):
                        
                        #print(data['Test'][insertion_columns_types[i]][st.session_state['gender']][str(k)])
                        if value_orig > data['Test'][insertion_columns_types[i]][st.session_state['gender']][str(k)]:
                            value = k
                            break
                        else:
                            pass
                else:
                    for k in range(1, 5):
                        if value_orig > data['Test'][insertion_columns_types[i]][st.session_state['gender']][str(k)]:
                            value = k
                            break
                        else:
                            pass

                #1
                insertion[j] = value
            except Exception as e:
                #print(e)
                insertion[j] = None
        df.insert(insertion_columns[i]+counter, insertion_columns_names[i], insertion)
        counter += 1

    return(df)
    # Функция для построения гистограммы
def plot_histogram(data, name):
    try:
        fig, ax = plt.subplots()
        ax.hist(data, bins=10, edgecolor='black')

        ax.set_xlabel('Marks')
        ax.set_ylabel('Frequency')
        ax.set_title('Marks Distribution for ' + name)
    except:
        pass

    st.pyplot(fig)

def main():
    st.title("Physical education estimation")
    # Выбор пола
    gender = st.selectbox("Выберите", ["Юноши", "Девушки"])
    st.session_state['gender'] = gender

    # Загрузка файла
    uploaded_file = st.file_uploader("Choose a XLSX file", type="xlsx")

    if uploaded_file is not None:
        # Load CSV file
        df = pd.read_excel(uploaded_file)
        df = predict_marks(df)
        # Display DataFrame
        st.write("### DataFrame:")
        st.dataframe(df)

        # Опции и информация о DataFrame
        st.sidebar.markdown("### Options:")
        show_info = st.sidebar.checkbox("Show DataFrame Info")
        if show_info:
            st.sidebar.write("### DataFrame Info:")
            st.sidebar.write(df.info())
        # Построение гистограмм
        filtered_columns = [col for col in df.columns if 'оценка' in col]
        #print(filtered_columns)
        for k in filtered_columns:
            plot_histogram(df[k], k)
        # Вызов основной функции
if __name__ == "__main__":
    main()