import ast
import re


def adresa_u_index(adresa):
    adresa = adresa.lower()
    i = 0
    while i < len(adresa) and adresa[i].isalpha():
        i += 1
    slova = adresa[:i]
    brojevi = adresa[i:]
    
    stupac = 0
    for znak in slova:
        stupac = stupac * 26 + (ord(znak) - ord('a') + 1)
    stupac -= 1  

    red = int(brojevi) - 1  
    return (red, stupac)

def evaluiraj_izraz(izraz, varijable={}):
        
    # jedan cool dodatak koji mi je pao na pamet:
    if izraz.startswith("SUM(") and izraz.endswith(")"):
        raspon = izraz[4:-1]
        if ':' in raspon:
            start, end = raspon.split(':')
            red1, kol1 = adresa_u_index(start)
            red2, kol2 = adresa_u_index(end)

            ukupno = 0
            for r in range(min(red1, red2), max(red1, red2) + 1):
                for k in range(min(kol1, kol2), max(kol1, kol2) + 1):
                    cell = varijable['sheet'].celije[r][k]
                    val = cell.value if cell.value is not None else 0
                    ukupno += val
            return ukupno
        else:
            raise Exception("Neispravan SUM izraz.")
        
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):  
            return node.value
        elif isinstance(node, ast.Name):
            if node.id not in varijable:
                raise KeyError(f"Nepoznata referenca: {node.id}")
            val = varijable[node.id]
            if val is None:
                raise ValueError(f"Ćelija '{node.id}' je prazna!")
            return val
        elif isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Add):
                return _eval(node.left) + _eval(node.right)
            elif isinstance(node.op, ast.Sub):
                return _eval(node.left) - _eval(node.right)
            elif isinstance(node.op, ast.Mult):
                return _eval(node.left) * _eval(node.right)
            else:
                raise Exception("Koristeni operator nije podrzan")
        else:
            raise Exception('Nepodržan izraz')

    stablo = ast.parse(izraz, mode='eval')
    return _eval(stablo.body)

class Cell:
    def __init__(self, sheet, row= None, col= None):
        self.sheet = sheet
        self.row = row
        self.col = col
        self.exp = None
        self.value = None
        self.dependenticies = set()
        self.visited = False
    
    def __str__(self):
        return f"[{self.exp} - cash: {self.value}] "
    
    def set_content(self, content):
        self.exp = content.upper()
        self.value = None
        self.sheet.evaluate(self)
        self.propogate()

    def propogate(self):
        for cell in self.dependenticies:
            cell.update()
    
    def update(self):
        self.value = None
        self.sheet.evaluate(self)
        self.propogate()

    def get_adress(self):
        return chr(ord('A') + self.col) + str(self.row + 1)


class Sheet:
    def __init__(self, br_red, br_stupac):
        self.celije = [ [Cell(self, r, s) for s in range(br_stupac)] for r in range(br_red)]

    def print_sheet(self):
        print()
        print("Ipis trenute tablice:")
        for red in self.celije:
            for i in red:
                print(i, end="")
            print()
        print()

    def cell_ref(self, adresa):
        (red, stupac) = adresa_u_index(adresa)
        try:
            return self.celije[red][stupac]
        except IndexError as e:
            raise IndexError("Ne postoji celija na toj adresi")
    
    def cell_set(self, adresa, content):
        print(f"Postvaljam izraz {content} na adresu {adresa}")
        celija = self.cell_ref(adresa)
        celija.set_content(content)

    def cell_get_refs(self, cell):
        if not cell.exp:
            return []
        adrese = re.findall(r"[A-Z]+[0-9]+", cell.exp)
        rezultat = []
        for ozn in adrese:
            used_cell = self.cell_ref(ozn)
            used_cell.dependenticies.add(cell)
            rezultat.append(used_cell)
        return rezultat

    def evaluate(self, cell):
        if cell.visited:
            raise RuntimeError(f"Otkrivena kružna ovisnost u ćeliji: {cell.get_adress()}")
        if cell.value is not None:
            return cell.value

        cell.visited = True 

        if not cell.exp:  
            cell.value = None
            cell.visited = False
            return None

        references = self.cell_get_refs(cell)

        varijable = {'sheet': self}
        for ref_cell in references:
            vrijednost = self.evaluate(ref_cell)
            if vrijednost is None:
                raise ValueError(f"Ćelija {ref_cell.get_adress()} je prazna, a koristi se u izrazu za {cell.get_adress()}")
            varijable[ref_cell.get_adress().upper()] = vrijednost

        cell.value = evaluiraj_izraz(cell.exp, varijable)
        cell.visited = False 
        return cell.value
    
def main():
    sheet = Sheet(5, 5)
    sheet.print_sheet()
    sheet.cell_set("A1", "5")
    sheet.cell_set("A2", "5")
    sheet.cell_set("A3", "A1+A2")
    sheet.print_sheet()
    
    sheet.cell_set("B1", "A1")
    sheet.cell_set("B2", "2")
    sheet.print_sheet()
    sheet.cell_set("B3", "B1+B2+A3")
    sheet.print_sheet()
    sheet.cell_set("A1", "4")
    sheet.print_sheet()

    sheet.cell_set("C1", "3")
    sheet.cell_set("C2", "7")
    sheet.cell_set("C3", "C1*C2")
    sheet.print_sheet()

    sheet.cell_set("C1", "2")
    sheet.print_sheet()

    #dodatno:
    sheet.cell_set("A4", "SUM(A1:A3)")             
    sheet.print_sheet()

    # testiram da radi za ciklicku ovisnost:
    try:
        sheet.cell_set('A1', 'A3')
    except RuntimeError as greska:
        print("Greska uhvacena:", greska)

if __name__ == "__main__":
    main()

# Komentar:

# Moj program koristi Observer obrazac (obrazac promatrača).
# Svaka ćelija (`Cell`) zna tko ovisi o njoj (putem `dependenticies`),
# i kada se njezin sadržaj promijeni, automatski obavještava sve ovisne ćelije da se ponovno izračunaju.
# Time se postiže automatsko ažuriranje vrijednosti kroz sve lance ovisnosti.