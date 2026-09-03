from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import os
from flask import jsonify


from flask import Flask, render_template, redirect, url_for, request
from models import db, Post, Comment
from forms import CommentForm
from flask_sqlalchemy import SQLAlchemy



# from pylatexenc.latexwalker import LatexWalker, LatexMacroNode, LatexCharsNode


app = Flask(__name__, static_url_path='/static')



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




db = SQLAlchemy(app)

# Load the dataset
data1 = pd.read_csv("design_principles_coding.csv", delimiter=";")

# Sort the data by the 'index' column
data1.sort_values(by='index', inplace=True)

data = data1

# Qualities mapping from thesis diagram (design principle index numbers)
QUALITY_GROUPS = [
    {"name": "Human-oriented", "indices": [7, 27]},
    {"name": "Reconfiguration", "indices": [11, 13, 14, 15, 16, 17, 18, 19, 26]},
    {"name": "Scatteredness", "indices": [2, 3, 4, 5]},
    {"name": "Event visibility", "indices": [6, 24]},
    {"name": "Connection", "indices": [8, 9, 10, 20, 21, 22, 23, 25]},
    {"name": "Flexible use", "indices": [1, 12]},
]


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('index_2.html', post=post, form=form)


@app.route('/')
def index():
    # Get the selected dimension from the query string
    selected_dimension = request.args.get('dimension')

    if selected_dimension == 'Qualities':
        quality_groups = []
        for group in QUALITY_GROUPS:
            # Map design-principle index numbers → dataframe row positions
            row_indices = []
            for principle_index in group["indices"]:
                matches = data.index[data['index'] == principle_index].tolist()
                row_indices.extend(matches)
            quality_groups.append({"name": group["name"], "indices": row_indices})
        return render_template(
            'index_2.html',
            data=data,
            groups=[],
            quality_groups=quality_groups,
            selected_dimension='Qualities',
        )

    if selected_dimension is None or selected_dimension not in data.columns:
        # If no dimension selected or invalid dimension, render the default view
        return render_template('index_2.html', data=data, groups=[], quality_groups=None)

    # Group the design principles based on the selected dimension
    groups = []
    for value in data[selected_dimension].unique():
        group_indices = data[data[selected_dimension] == value].index.tolist()
        groups.append(group_indices)

    return render_template(
        'index_2.html',
        data=data,
        groups=groups,
        quality_groups=None,
        selected_dimension=selected_dimension,
    )




# 下面是基于 分开文件夹的csv
@app.route('/detail_2/<int:index>')
def detail_2(index):
    principle = data.iloc[index]

    folder_path = f"static/image/{principle['detail_pictures_folder']}"
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpeg') or f.endswith('.jpg') or f.endswith('.png')]

    description_csv_path = os.path.join(folder_path, 'description.csv')
    image_descriptions = {}

    if os.path.exists(description_csv_path):
        description_df = pd.read_csv(description_csv_path)
        image_descriptions = dict(zip(description_df['filename'], description_df['description']))
        print(f"Descriptions loaded: {image_descriptions}")  # Debug print
    else:
        print(f"CSV file not found at path: {description_csv_path}")  # Debug print

    return render_template('detail_2.html', principle=principle, image_files=image_files, image_descriptions=image_descriptions, data=data)














@app.route('/rearrange', methods=['POST'])
def rearrange():
    new_order = request.json['newOrder']  # Get the new order of design principles
    updated_data = data.iloc[new_order]  # Rearrange the data according to the new order
    return updated_data.to_json(orient='records')

# @app.route('/get_available_themes')
# def get_available_themes():
#     # Extract all unique themes from the '(Other) Themes' column
#     available_themes = set()
#     for themes_str in data['(Other) Themes']:
#         themes = themes_str.split('/')
#         available_themes.update(themes)
#     # return jsonify(list(available_themes))
#     return list(available_themes)




@app.route('/get_available_themes')
def get_available_themes():
    # Extract all unique themes from the '(Other) Themes' column
    available_themes = set()
    for themes_str in data['(Other) Themes']:
        themes = themes_str.split('/')
        available_themes.update(themes)
        list_available_themes = list(available_themes)
    return jsonify(list_available_themes)

@app.route('/filter_by_theme', methods=['POST'])
def filter_by_theme():
    selected_theme = request.json['theme']  # Get the selected theme
    filtered_principles = data[data['(Other) Themes'].str.contains(selected_theme)]

    return render_template('themes.html', data=filtered_principles, theme=selected_theme)



@app.route('/event_typology')
def event_typology():
    return send_from_directory('templates', 'event_typology.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG') == '1')









#
# # 下面是基于用合并文本的csv
#
# data_descriptions = pd.read_csv("design_principles_descriptions.csv")
#
# @app.route('/detail_2/<int:index>')
# def detail_2(index):
#     principle = data.iloc[index]
#     principle_name = principle['design_principle_name']
#     principle_description = get_description(principle_name)
#
#     # Filter images based on naming convention
#     folder_path = "static/image"
#     image_files = [f for f in os.listdir(folder_path) if
#                    f.startswith(principle_name) and (f.endswith('.jpeg') or f.endswith('.jpg') or f.endswith('.png'))]
#
#     return render_template('detail_2.html', principle=principle, image_files=image_files,
#                            principle_description=principle_description)
#
#
# def get_description(principle_name):
#     principle = data_descriptions[data_descriptions['design_principle_name'] == principle_name]
#     if not principle.empty:
#         return principle['description'].iloc[0]
#     else:
#         return 'Description not found'





# #下面是用latex渲染的detail page
#
# def parse_latex_subsections(latex_content):
#     walker = LatexWalker(latex_content)
#     nodes, _, _ = walker.get_latex_nodes()
#
#     descriptions = {}
#     current_principle = None
#     current_description = []
#
#     for node in nodes:
#         if isinstance(node, LatexMacroNode) and node.macroname == 'subsubsection':
#             if current_principle:
#                 descriptions[current_principle] = '\n'.join(current_description).strip()
#             current_principle = ''.join(child.chars for child in node.nodeargd.argnlist[0].nodelist if
#                                         isinstance(child, LatexCharsNode)).strip()
#             current_description = []
#         elif isinstance(node, LatexCharsNode):
#             current_description.append(node.chars)
#         elif isinstance(node, LatexMacroNode) and node.macroname == 'label':
#             continue
#
#     if current_principle:
#         descriptions[current_principle] = '\n'.join(current_description).strip()
#
#     return descriptions
#
#
# @app.route('/detail_2/<int:index>')
# def detail_2(index):
#     principle = data.iloc[index]
#
#     # Load and parse the LaTeX document containing all descriptions
#     with open('main.tex', 'r') as file:
#         latex_content = file.read()
#
#     descriptions = parse_latex_subsections(latex_content)
#
#     principle_name = principle['design_principle_name'].strip()  # Normalize the name
#     principle_description = descriptions.get(principle_name, 'Description not found')
#
#     # Filter images based on naming convention
#     folder_path = "static/image"
#     image_files = [f for f in os.listdir(folder_path) if
#                    f.startswith(principle_name) and (f.endswith('.jpeg') or f.endswith('.jpg') or f.endswith('.png'))]
#
#     return render_template('detail_2.html', principle=principle, image_files=image_files,
#                            principle_description=principle_description, data=data)
#


