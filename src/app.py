'''
 # @ Create Time: 2023-06-09 21:22:21.314123
'''

import pathlib
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__, title="Gambling_Project")

df = pd.read_csv('https://docs.google.com/spreadsheets/d/1jK_z5sy4XxaUru3LU69a8ryy04Tf10gf0sCy2xev_EE/gviz/tq?tqx=out:csv&sheet=Sheet3')
df = df.T.reset_index()
df.columns = df.iloc[0].values
df =  df.iloc[2:]
weeks = '''13.03-19.03	20.03-26.03	27.03-02.04	03.04-09.04	10.04-16.04	17.04-23.04	24.04-30.04	01.05-07.05	08.05-14.05	15.05-21.05	22.05-28.05	29.05-04.06'''.split('	')
cls = df.columns.values
regs = cls[1:4]
dep = cls[5:8]
gmrs = cls[8:11]
rev = [cls[4]] + list(cls[11:])

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

def load_data(data_file: str) -> pd.DataFrame:
    '''
    Load data from /data directory
    '''
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    return pd.read_csv(DATA_PATH.joinpath(data_file))

app.layout = html.Div(
    children=[
        html.H1('Показатели Проекта'),
        html.Div([
        dcc.Markdown('''В верхнем правом углу каждой таблицы есть инструменты навигации, позволяющие приближать или отдалять график
        Справа можно выбрать тот или иной показатель, отобразив или скрыв его на графике. Графики интерактивные, можно посмотреть показатель в определенный момент времени
        Первый график показывает основную информацию: Регистрации и Конверсии. Далее можно выбрать иные показатели из таблицы
        Любые вопросы вы можете задать [в моем телеграмме](https://t.me/kiradas)

        Я немного отредактировал определенно некорректные данные (общее число показателя меньше, чем его положительные составляющие). Данный инструмент полностью бесплатен и 
        предоставляет больше возможнстей, чем эксель. На реальном проекте с корректными данными я бы добавил больше функций и улучшил визуализацию
        ''')
    ]),
        html.Div([
            dcc.Graph(
                figure=dict(
                    data=[
                        dict(
                        x=weeks,
                        y=df[regs[0]],
                        type='scatter',
                        mode='none',
                        fill='tonexty',
                        name=regs[0]
                    ),
                    dict(
                        x=weeks,
                        y=df[regs[1]],
                        type='scatter',
                        mode='none',
                        fill='tozeroy',
                        name=regs[1]
                    ),
                    dict(
                        x=weeks,
                        y=df[regs[2]],
                        type='scatter',
                        mode='lines',
                        yaxis='y2',
                        name=regs[2]
                    )
                ],
                    layout=dict(
                    title='Регистрации и Конверсия',
                    xaxis=dict(title='Недели'),
                    yaxis=dict(title='Регистрации'),
                    yaxis2=dict(title='Конверсия', overlaying='y', side='right')
                    )
                )
            )
        ]),
        html.P("Выберите данные:"),
        html.Div([
            dcc.Dropdown(
                id='y-axis-dropdown',
                options=[#{'label': 'Регистрации', 'value': 'regs'},
                  {'label': 'Депозиты', 'value': 'dep'},
                  {'label': 'Игроки', 'value': 'gmrs'},
                  {'label': 'Доходы и затраты', 'value': 'rev'}
                ],
                value='dep'
            ),
            dcc.Graph(id='data-visualization')
            
        ])
    ]
)

@app.callback(
    Output('data-visualization', 'figure'),
    [Input('y-axis-dropdown', 'value')]
)
def update_graph(selected_reg):
    lbl = {#'regs':'Регистрации',
           'dep':'Депозиты',
          'gmrs': 'Игроки',
          'rev': 'Доходы и затраты'}[selected_reg]
    selected_reg = {#'regs':regs,
                    'dep':dep,
                    'gmrs': gmrs,
                    'rev': rev}[selected_reg]
              

    rgs = [[max(df[selected_reg[x]].astype(int)), x] for x in range(3)]
    rgs = pd.DataFrame(rgs, columns=['First', 'Second'])
    sorted_df = rgs.sort_values(by='First', ascending = False)
    sorted_array = sorted_df['Second'].values.tolist()
    #print(sorted_array)

    data = [
        dict(
            x=weeks,
            y=df[selected_reg[sorted_array[2]]],
            type='scatter',
            mode='lines',
            yaxis='y2',
            name=selected_reg[sorted_array[2]]
        ),
        dict(
            x=weeks,
            y=df[selected_reg[sorted_array[1]]],
            type='scatter',
            mode='markers',
            fill='tonexty',
            name=selected_reg[sorted_array[1]]
        ),
        dict(
            x=weeks,
            y=df[selected_reg[sorted_array[0]]],
            type='scatter',
            mode='markers',
            fill='tonexty',
            name=selected_reg[sorted_array[0]]
        )
    ]
    
    layout = dict(
        title=lbl +' и ' + selected_reg[sorted_array[2]],
        xaxis=dict(title='Недели'),
        yaxis=dict(title=lbl ),
        yaxis2=dict(title=selected_reg[sorted_array[2]], overlaying='y', side='right')
    )
    
    return dict(data=data, layout=layout)


if __name__ == "__main__":
    app.run_server(debug=True)
