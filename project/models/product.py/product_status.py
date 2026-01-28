
from enum import Enum
    
class ProductStatus(Enum):
    """
    Representa os possíveis estados de um produto no sistema.
    - ACTIVE: Produto ativo e disponível para venda.
    - INACTIVE: Produto inativo, não disponível para venda.
    - BLOCKED: Produto bloqueado por motivos administrativos ou operacionais.
    - DISCONTINUED: Produto descontinuado, não é comercializado.
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    DISCONTINUED = "discontinued"