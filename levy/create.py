import pandas as pd
import os

def createPlugin(args):
    source = args.source
    if source not in os.listdir():
        print('Source not found in current directory')
        return
    df = pd.read_csv(source)
    print("{} no of plugin is to be generated".format(len(df)))
    for idx in range(0, len(df)):
        template = ""
        with open("./templates/php_boilerplate.tem", "r+") as t:
            template = t.read()
        url = df.iloc[idx]['url']
        plugin_name = df.iloc[idx]['plugin name']
        country = df.iloc[idx]['country']
        columns = df.iloc[idx]['columns']
        pid = df.iloc[idx]['pid']
        jira = df.iloc[idx]['jira']
        proxy = df.iloc[idx]['proxy']
        colnames = columns.split(",")
        columns = ", ".join(["'{}'".format(x) for x in colnames])
        template = template.replace("%URL%","{}".format(url))
        template = template.replace("%PLUGINNAME%", "{}".format(plugin_name))
        template = template.replace("%PID%", "{} force".format(pid))
        template = template.replace("%COUNTRY%", "{}".format(country.upper()))
        template = template.replace("%JIRATICKET%", "{}".format(jira))
        template = template.replace("%PROXY%", "{}".format(proxy))
        template = template.replace("%COLUMNS%", "{}".format(columns))

        arrentry = ""
        for col in colnames:
            arrentry = "{}$arr['{}'] = $data['{}'];\n\t\t\t".format(arrentry, col, col)

        template = template.replace("%ARRENTRY%", arrentry)
        folderpath = args.dir
        if folderpath == "":
            folderpath = "./"
        newpath = "{}{}/".format(folderpath, plugin_name)
        os.mkdir(newpath)
        newfilename = "{}{}.php".format(newpath, plugin_name)
    
        with open(newfilename, "w") as f:
            f.write(template)
