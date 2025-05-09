import os 
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def open_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            raw_data: dict = json.load(json_file)

            # Only save if 'istemplate' is True and 'datafim' does not exist 

            if raw_data['istemplate'] != True:
                print(f'{json_path} istemplate = False')
                return 
            
            for step in raw_data['quest_steps']:
                for content in step['n_contents']:
                    data = {}
                    data['quest_id'] = raw_data.get('id', '')
                    data['quest_nome'] = raw_data.get('nome', '').replace('\n', ' ')
                    data['materia'] = raw_data.get('rel_materia', {}).get('nome', '').replace('\n', ' ')
                    data['ano_escolar'] = raw_data.get('rel_anoescolar', {}).get('nome', '').replace('\n', ' ')

                    data['nome_etapa'] = step.get('apelido', '').replace('\n', ' ')

                    data['content_ativo'] = content.get('ativo', '').replace('\n', ' ')
                    data['content_nome'] = content.get('description', '').replace('\n', ' ')


                    if content['content_type'] != 0:
                        continue

                    obj = {
                        0: "Escolha Única",
                        1: "Verdadeiro/Falso",
                        2: "Múltipla Escolha",
                        3: "Preencha as Lacunas",
                        4: "Correspondente",
                        5: "Imagens Correspondentes",
                        6: "Ordenação",
                        7: "Dissertativa"
                    }

                    raw_question_type = content['question_type']

                    question_type = obj[raw_question_type]

                    data['question_type'] = question_type

                    data['answer_options'] = {}
                
                    key = 1
                    for answer in content['relx_answers']:
                        
                        datafim_answer = answer.get('datafim')

                        if datafim_answer is not None:
                            continue

                        data['answer_options'][key] = answer.get('titulo', '').replace('\n', ' ')
                        key += 1
                        print(data['answer_options'])
                        # data['answer_options'].append(answer.get('titulo', '').replace('\n', ' '))

                        if answer.get('resposta_correta') == True:
                            data['reposta_correta'] = answer.get('titulo', '')



                    # Only save if 'istemplate' is True and 'datafim' does not exist 
                    datafim = (
                        raw_data.get('datafim')
                        or step.get('datafim')
                        or content.get('datafim')
                    )

                    if datafim is not None:
                        print(f'{json_path} datafim is not None')


                    if datafim is None:

                        all_rows.append(data)
            
            return
    
    except Exception as e:
        print(f"Deu erro em {json_path} - Error: {e}")
        return


def write_excel(xlsx_path, all_data):
    try:
        df = pd.DataFrame(all_data)
        df.to_excel(xlsx_path, index=False)
        print("Sucessuful operation")
        print(f"saved in {xlsx_path} ")
    except Exception as e:
        print(f"ERROR IN  XLSX - Error: {e}")

all_rows = []

xlsx_path =  os.getenv("XLSX_PATH") #path of the csv file
folder_path = os.getenv("FOLDER_PATH") #path to the folder of the jsons files

i = 0
for file in os.listdir(folder_path):
    json_path = os.path.join(folder_path, file)
    open_json(json_path)
    if i == 00:
        break
    i += 1

write_excel(xlsx_path, all_rows)
