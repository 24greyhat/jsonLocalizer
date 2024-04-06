from googletrans import Translator
import json
import os
import sys



class JsonLocalizer:
    def __init__(self, json_file_path):
        self.path = json_file_path
        self.lpath = "./languages.json"
        self.translator = Translator()

    
        if os.path.exists(self.path) and os.path.exists(self.lpath):
            with open(self.path) as f:
                self.main_json = json.load(f)

            with open(self.lpath) as f1:
                self.languages = json.load(f1)

        else:
            print(f"can't find json file at: \"{self.path}\" or maybe the languages.json file is missing!")
            sys.exit(1)


    def localize(self, entryKey):
        languages = "export const languages = [\n"
        if not os.path.exists("translations"):
            os.mkdir("translations")
            with open("translations/index.js", "w") as f:
                f.write("")
            with open("translations/languages.js", 'w') as f:
                f.write("")

        for lang in self.languages:
            print(f"\n\nTransalting to: {lang['name']}")

            try:
                test = self.translator.translate("test", dest=lang['code'])
            except ValueError:
                print(f"\n[-] Failed\n")
                continue


            languages+=str(lang)+",\n"

            path = f"translations/{lang['code'].replace('-', '')}.json"
            c = self.main_json.copy()
            current = c[entryKey].values()

            c.update({"language": lang['name']})

            if lang['code'] != "en":
                for d in current:
                    for k,v in zip(d.keys(), d.values()):
                        r = self.translator.translate(v, dest=lang['code'])
                        d.update({k:r.text})


            print("\n[+] Done\n")

            with open(path, 'w') as f:
                json.dump(c, f, ensure_ascii=False, indent=4)

            with open("translations/index.js", "a") as f1:
                s = "export "+"{ default as "+lang['code'].replace("-", "")+' }'+' from \"'+"./"+lang['code'].replace("-", "")+'.json'+'"'+';\n' 
                f1.write(s)



        with open('translations/languages.js', 'a') as f2:
            f2.write(languages+"\n]")

        with open('translations/en.json') as f3:
            json.dump(self.main_json, f3)


    
