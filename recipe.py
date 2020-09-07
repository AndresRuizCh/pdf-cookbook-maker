import pandas as pd
import numpy as np
import hashlib
import shutil
import getopt
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class CookBook(object):
    """Cookbook PDF-LaTeX Generator. Hosted on https://github.com/AndresRuizCh/pdf-cookbook-maker
        
       Input:
        - title : (str) title of the cookbook (default "My Cookbook")
        - author : (str) author of the cookbook (default "Author")
        - ingredients_keyword : (str) keyword for the ingredients title (default "Ingredients")
        - steps_keyword : (str) keyword for the steps title (default "Steps")
        - language : (str) language for rendering the LaTeX document in ISO format (default "en-EN")
        - source_route : (str) route of the database (default "Recipes.csv")
        - tex_route : (str) route of the LaTeX folder (default "tex")
        - pdf_name : (str) name of the pdf"""

    def __init__(self, title="My Cookbook", author="Author", ingredients_keyword="Ingredients", steps_keyword="Steps",
                 language="english", source_route="Recipes.csv", tex_route="tex", pdf_name="Recipes.pdf"):

        if '.csv' in source_route:
            self.df = pd.read_csv(source_route)
        else:
            self.df = pd.read_excel(source_route)

        self.title = title
        self.author = author
        self.source_route = source_route
        self.ingredients_keyword = ingredients_keyword
        self.steps_keyword = steps_keyword
        self.language = language
        self.tex_route = tex_route
        self.pdf_name = pdf_name.replace(".pdf", "")

    def from_csv(self):

        """ Reads the excel file from config folder and fills the picture field """

        def picture(name):
            return self.tex_route + "\\pictures\\" + hashlib.md5(name.encode('utf-8')).hexdigest() + ".jpg"

        for i in self.df[self.df["Image"].isnull()].index.values:
            file = input("Enter path of the picture " + ' (' + self.df.loc[i, "Recipe"] + ')' + ': ')
            newfile = picture(self.df.loc[i, "Recipe"])
            shutil.copy(file, newfile)
            self.df.loc[i, "Image"] = newfile

        self.df["Image"] = self.df["Recipe"].apply(lambda x: picture(x))
        self.df = self.df.sort_values(["Section", "Subsection", "Recipe"])

        if '.csv' in self.source_route:
            self.df.to_csv(self.source_route, index=False)
        else:
            self.df.to_excel(self.source_route, index=False)

    def to_latex(self):

        """ Generates a PDF file for the recipe book. You must have a LaTeX compiler installed."""

        with open(self.tex_route + "\\" + "preamble.tex", "rb") as pre:
            pre = pre.read().decode('utf-8')
            preamble = pre.replace("Book_Title_Placeholder", self.title)
            preamble = preamble.replace("Book_Author_Placeholder", self.author)
            preamble = preamble.replace("Language_Placeholder", self.language)

        self.df = self.df.set_index(["Section", "Subsection"])
        body = ''

        for i in self.df.index.levels[0].tolist():
            body += '\\part{' + i + '}\n'

            for j in sorted(set(self.df.loc[i].index.tolist())):
                body += '\\chapter{' + j + '}\n'
                values = self.df.loc[i].loc[j].values

                if np.ndim(values) == 1:
                    values = [values]

                for k in values:
                    body += '\n\\newpage\n\\section{' + str(k[0]) + '}\n' + '\\begin{center} \\large ' + str(k[1]) + \
                            ' - ' + str(k[2]) + ' - ' + str(k[3]) + ' \\end{center}\n' + \
                            '\\subsection{' + self.ingredients_keyword + '} \n' + \
                            '\\begin{minipage}{0.5\\textwidth} \n\\begin{itemize}\n'

                    for ingred in str(k[4]).split('; '):
                        body += '\\item ' + ingred + '\n'

                    body += '\\end{itemize}\n\\end{minipage}\n\\begin{minipage}{0.5\\textwidth}\n' + \
                            '\\includegraphics[width=0.9\\linewidth]{' + \
                            k[6].replace(self.tex_route + '\\', '').replace('\\', '/') + '}\n\\end{minipage}\n' + \
                            '\\linespread{1.25}\n\\subsection{' + self.steps_keyword + '}\n\\begin{itemize}\n'

                    for step in str(k[5]).split('; '):
                        body += '\\item ' + step + '.\n'

                    body += '\\end{itemize}\n'

        body = preamble + body + '\n\\end{document}'

        with open(self.tex_route + "\\" + self.pdf_name + ".tex", "wb") as tex_file:
            tex_file.write(body.encode("utf-8"))

        os.system("cd " + self.tex_route + "& pdflatex " + self.pdf_name + ".tex & pdflatex " +
                  self.pdf_name + ".tex & del " + self.pdf_name + ".aux & del " + self.pdf_name +
                  ".toc & del " + self.pdf_name + ".log  & del " + self.pdf_name + ".out")

        shutil.move(self.tex_route + '\\' + self.pdf_name + '.pdf', self.pdf_name + '.pdf')
        os.system("start " + self.pdf_name + ".pdf")


def main(argv):

    opts, args = getopt.getopt(argv, "hl:t:i:a:s:x:d:f:", ["language=", "title=", "ingredients=", "author=", "steps=",
                                                           "tex=", "database=", "file="])

    (language, title, ingredients, author, steps, tex, database, file) = ("english", "My Cookbook", "Ingredients",
                                                                          "Author", "Steps", "tex", "Recipes.csv",
                                                                          "Recipes.pdf")
    for opt, arg in opts:
        if opt == '-h':
            print('recipe.py -l <language> -t <title> -i <ingredients> -a <author> -s <steps> '
                  '-x <tex> -d <database> -f <file>')
            sys.exit()
        elif opt in ("-l", "--language"):
            language = arg
        elif opt in ("-t", "--title"):
            title = arg
        elif opt in ("-i", "--ingredients"):
            ingredients = arg
        elif opt in ("-a", "--author"):
            author = arg
        elif opt in ("-s", "--steps"):
            steps = arg
        elif opt in ("-x", "--tex"):
            tex = arg
        elif opt in ("-d", "--database"):
            database = arg
        elif opt in ("-f", "--file"):
            file = arg

    CB = CookBook(title, author, ingredients, steps, language, database, tex, file)
    CB.from_csv()
    CB.to_latex()


if __name__ == "__main__":
    main(sys.argv[1:])
