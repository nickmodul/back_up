import pandas as pd
from dataclasses import dataclass,field

def get_type(
        df                      :pd.DataFrame,
        column_name             :str,
        number_when_not_nominal :int=120
        ):
    
    if  df[column_name].value_counts().shape[0]<number_when_not_nominal:
        return 'nominal'
    else:
        return 'continue'
# get_type(process_data,'Код заявки')


def convert_table_er(
        df_name     :str,
        

        df          :pd.DataFrame,

        language    :str='rus'
        ):
    
    result_df = pd.DataFrame()
    # link_to_example:: https://docs.google.com/spreadsheets/d/1ts3ho_5pNMvIKuD_f3B6dtJRrYH7qJyaZUxZM8N2VtA/edit?usp=sharing

    for column in df.columns:
        unique_values = df[column].value_counts().reset_index()
        new_df = pd.DataFrame(unique_values)
        
        table_name = 'tab_' + language 
        # new_df[table_name] = new_df.columns[0]
        new_df[table_name] = df_name
        new_df['column_name'] = column
        
        new_df['type'] = df[column].dtype
        new_df['count_null'] = df[column].isna().sum()
        new_df['null_percent'] = ((new_df['count_null']/df.shape[0])*100).astype(int)

        new_df['discret_type'] =get_type(df=new_df, column_name=column)

        new_df = new_df.rename(columns=({new_df.columns[0]:'column_value','count':'count_unique_values'}))
        result_df = result_df._append(new_df, ignore_index=True) # type: ignore
        
    return result_df

def get_entity_table(df:pd.DataFrame):
    return df.groupby('column_name').head(1).reset_index()



@dataclass
class TABLE_VIEW:
    df_name: str
    df_input: pd.DataFrame
    result_table: pd.DataFrame | None= None
    entity_table: pd.DataFrame = field(default_factory=pd.DataFrame)
    def __post_init__(self):
        self.result_table = convert_table_er(df_name=self.df_name, df=self.df_input,)
        self.entity_table = self.result_table.groupby('column_name').head(1).reset_index().drop(columns='index')
    def generate_text_representation(self):

        text_representation = f'Table {self.df_name} {{\n'
        for index, row in self.entity_table.iterrows():
            text_representation += f'  {row["column_name_eng"]} {row["type"]}\n'

        # Add the line for the primary key
        text_representation += f'  id_{self.df_name} integer [primary key]\n'

        text_representation += '}\n'
        return text_representation
# # Example
# process_data = pd.DataFrame({'following_user_id': [1, 2, 3], 'followed_user_id': [4, 5, 6], 'created_at': ['2023-01-01', '2023-02-01', '2023-03-01']})
# my_table_view = TABLE_VIEW(
#     df_name='df_raw', 
#     df_input=process_data,
#     table_name='таблица заявок')
# print(my_table_view.generate_text_representation())
# print(my_table_view.entity_table.to_string)
