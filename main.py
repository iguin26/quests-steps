import os 
import json
import csv

def open_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            raw_data: dict = json.load(json_file)



            for step in raw_data['quest_steps']:
                for content in step['n_contents']:
                    for answer in content['relx_answers']:

                        data = {}
                        data['quest_id'] = raw_data.get('id', '')
                        data['quest_nome'] = raw_data.get('nome', '').replace('\n', ' ')
                        data['materia'] = raw_data.get('rel_materia', {}).get('nome', '').replace('\n', ' ')
                        data['ano_escolar'] = raw_data.get('rel_anoescolar', {}).get('nome', '').replace('\n', ' ')

                        data['nome_etapa'] = step.get('apelido', '').replace('\n', ' ')

                        data['content_ativo'] = content.get('ativo', '').replace('\n', ' ')
                        data['content_nome'] = content.get('description', '').replace('\n', ' ')

                        
                        data['answer_texto'] = answer.get('titulo', '').replace('\n', ' ')  
                        data['answer_correct'] = answer.get('resposta_correta', '') 

                        all_rows.append(data)
    
    except Exception as e:
        print(f"Deu erro em {json_path} - Error: {e}")




def write_csv(csv_path, all_data):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        try: 
            fieldnames = ['quest_id', 'quest_nome', 'materia', 'ano_escolar', 
                          'nome_etapa', 'content_ativo', 'content_nome', 
                          'answer_texto', 'answer_correct']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)

        except Exception as e:
          print(f"Deu erro NA HORA DE COLOCAR NO CSV  - Error: {e}")




all_rows = []

csv_path = '/home/kakaiser/iguin/dev/python/extract_json_files/aulas.csv'

folder_path = '/home/kakaiser/Documents/json/'

i = 0
for file in os.listdir(folder_path):
    json_path = os.path.join(folder_path, file)
    open_json(json_path)
    # if i == 200:
    #     break
    # i += 1

write_csv(csv_path, all_rows)