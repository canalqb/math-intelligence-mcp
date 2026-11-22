"""Math Intelligence MCP - Criptografia Avançada

Módulo P1 - Tool: advanced_cryptography
Implementações criptográficas: exponentenciação modular, ordens, logarítmo discreto.
"""

from typing import Dict, Any, Optional
import hashlib


def modular_exponentiation(base: int, exponent: int, modulus: int) -> Dict[str, Any]:
    """Calcula (base^exponent) % modulus usando exponenciação modular rápida."""
    try:
        if modulus <= 0:
            return {"success": False, "error": "Modulus deve ser positivo"}

        result = pow(base, exponent, modulus)

        return {
            "success": True,
            "base": base,
            "exponent": exponent,
            "modulus": modulus,
            "result": result,
            "formula": f"({base}^{exponent}) % {modulus} = {result}",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def discrete_logarithm(g: int, h: int, p: int, limit: Optional[int] = None) -> Dict[str, Any]:
    """Calcula logaritmo discreto: encontre x tal que g^x ≡ h (mod p).
    
    Usa o algoritmo baby-step giant-step ou força bruta para números pequenos.
    
    Args:
        g: Base
        h: Resultado
        p: Primo modulus
        limit: Limite superior para busca (padrão: p-1)
    
    Returns:
        Dict com success, exponent, steps
    """
    try:
        if p <= 0:
            return {"success": False, "error": "Prime modulus must be positive"}

        if limit is None:
            limit = p - 1

        # Normalizar h para o intervalo [0, p-1]
        h = h % p

        # Busca baby-step giant-step ( mais eficiente que força bruta)
        import math
        n = int(math.ceil(math.sqrt(limit)))

        # Baby step: calcular g^j mod p para j = 0, 1, ..., n-1
        table: Dict[int, int] = {}
        power = 1
        for j in range(n):
            if power not in table:  # Guardar primeira ocorrência
                table[power] = j
            power = (power * g) % p

        # Giant step: para cada i = 0, 1, ..., n-1, verificar se h * g^(-i*n) está na tabela
        # Calcular g^(-n) mod p usando inverso modular
        g_inv_n = pow(g, -n, p)  # Python 3.8+ poderá calcular inverso modular negativo

        target = h
        for i in range(n):
            if target in table:
                x = i * n + table[target]
                if x < p:
                    return {
                        "success": True,
                        "base": g,
                        "result": h,
                        "modulus": p,
                        "exponent": x,
                        "method": "baby-step giant-step",
                        "steps": f"encontrado após {i} iterações giant-step + {table[target]} baby-steps",
                    }

            # Próximo giant step: multiplicar por g^(-n)
            target = (target * g_inv_n) % p

        return {
            "success": False,
            "error": "Logaritmo discreto não encontrado dentro do limite especificado",
            "base": g,
            "result": h,
            "modulus": p,
            "searched_up_to": limit,
        }

    except ValueError as e:
        return {"success": False, "error": f"Erro de valor: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def hash_data(data: str, algorithm: str = "sha256") -> Dict[str, Any]:
    """Gera hash de dados usando algoritmo especificado."""
    try:
        if algorithm.lower() == "sha256":
            hash_obj = hashlib.sha256(data.encode("utf-8"))
        elif algorithm.lower() == "sha1":
            hash_obj = hashlib.sha1(data.encode("utf-8"))
        elif algorithm.lower() == "md5":
            hash_obj = hashlib.md5(data.encode("utf-8"))
        else:
            return {
                "success": False,
                "error": f"Algorithm '{algorithm}' não suportado",
                "data": data,
            }

        return {
            "success": True,
            "algorithm": algorithm.lower(),
            "data": data,
            "hash": hash_obj.hexdigest(),
            "hash_bytes": hash_obj.digest(),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def advanced_crypto_operation(operation: str, key: str = "", base: int = None, exponent: int = None, modulus: int = None) -> Dict[str, Any]:
    """Wrapper para operações criptográficas avançadas.
    
    Args:
        operation: Tipo de operação ('modular_exponentiation', 'discrete_logarithm', 'hash', 'rsa_keygen')
        key: Chave (para operações que precisam)
        base: Base (para exponenciação modular)
        exponent: Expoente
        modulus: Módulo
    
    Returns:
        Dict com resultado da operação
    """
    try:
        if operation == "modular_exponentiation":
            if base is None or exponent is None or modulus is None:
                return {"success": False, "error": "modular_exponentiation requer base, exponent e modulus"}
            return modular_exponentiation(base, exponent, modulus)
        
        elif operation == "discrete_logarithm":
            if base is None or key is None or modulus is None:
                return {"success": False, "error": "discrete_logarithm requer base (g), key (h) e modulus (p)"}
            return discrete_logarithm(base, int(key), modulus)
        
        elif operation == "hash":
            if not key:
                return {"success": False, "error": "hash requer dados (key)"}
            return hash_data(key)
        
        elif operation == "rsa_keygen":
            bits = int(key) if key else 2048
            return rsa_key_generation(bits)
        
        else:
            return {"success": False, "error": f"Operação '{operation}' não suportada. Use: modular_exponentiation, discrete_logarithm, hash, rsa_keygen"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def rsa_key_generation(bits: int = 2048) -> Dict[str, Any]:
    """Gera chaves RSA (apenas estrutura - usa sympy para geração de primos)."""
    try:
        import sympy as sp

        # Gerar dois primos grandes
        p = sp.primerange(2 ** (bits // 4), 2 ** (bits // 4 + 1)).__next__()
        q = sp.primerange(2 ** (bits // 4), 2 ** (bits // 4 + 1)).__next__()

        # Garantir p != q
        while q == p:
            q = sp.primerange(2 ** (bits // 4), 2 ** (bits // 4 + 1)).__next__()

        n = p * q
        phi = (p - 1) * (q - 1)

        # Escolher e tal que 1 < e < phi e gcd(e, phi) = 1
        e = 65537  # Fermat prime comum

        # Calcular d tal que d * e ≡ 1 (mod phi)
        d = pow(e, -1, phi)

        public_key = (e, n)
        private_key = (d, n)

        return {
            "success": True,
            "key_size_bits": bits,
            "public_key": public_key,
            "private_key": private_key,
            "primes": {"p": p, "q": q},
            "phi": phi,
            "note": "Chaves geradas para demonstração - produção deve usar CSPRNG",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}