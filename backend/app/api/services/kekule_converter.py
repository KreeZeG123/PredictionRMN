from rdkit import Chem

def convert_smiles_to_kekule(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        raise ValueError("Invalid SMILES")
    Chem.Kekulize(mol, clearAromaticFlags=True)
    return Chem.MolToSmiles(mol, canonical=True, kekuleSmiles=True)
