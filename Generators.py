class generators:

    def __init__(self,text):
        self.text = text.get('text')

    def dork_Generator(self):
        directory = ["cadastros/","produtos/","products/","car/","carrinho/","admin/","administrator/"]
        nameFiles_paramters = [".php?", ".aspx?", ".asp?"]
        nameFiles = [".php", ".aspx", ".asp"]
        try:
            nameFile = self.text.split(" ")[1]
            paramter = self.text.split(" ")[2]
        except:
            return "*Scrutin : Error*\n\n*Syntax command* : `/dork [nameFile] [paramter]`\n*Example:* `/dork index id=`"
        
        dorks = []
        for file in nameFiles_paramters:
            for dirt in directory:
                dorks.append("inurl:/"+dirt+nameFile+file+paramter)
        
        for file in nameFiles:
            for dirt in directory:
                dorks.append("inurl:/"+dirt+nameFile+file)

        a = ''.join(['\n' + dork for dork in dorks])
        return "*Scrutin - Generators : Dork*\n\n*[+] Information [+]*\n\n* - Total : *`{0}`\n\n *[+] Results : *\n `{1}`".format(str(a.count('\n')),a)