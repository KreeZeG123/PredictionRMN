from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdchem

def convert_smiles_to_kekule(smiles: str):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            raise ValueError("Invalid SMILES or incorrect chemical structure")
        
        try:
            Chem.Kekulize(mol, clearAromaticFlags=True)
        except rdchem.KekulizationError as e:
            raise ValueError(f"Kekulization error: {str(e)}")
        
        return Chem.MolToSmiles(mol, canonical=True, kekuleSmiles=True)
    
    except ValueError as ve:
        raise ve
    except rdchem.RDKitError as re:
        raise ValueError(f"RDKit error: {str(re)}")
