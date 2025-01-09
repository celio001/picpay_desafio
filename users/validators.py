from django.core.exceptions import ValidationError

def validate_cpf(value):
    #remover pontucao
    cpf = ''.join([char for char in value if char.isdigit()])

    #verificar se tem 11 digitos
    if len(cpf) != 11:
        raise ValidationError('CPF inválido')
    
    #Verificar se todos os dígitos são iguais 
    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido')
    
    # Função para calcular os dígitos verificadores 
    def calcular_digito(cpf, multiplicadores):
        soma = sum(
            int(cpf[i]) * multiplicadores[i]
            for i in range(len(multiplicadores))
        )
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    # Multiplicadores para o primeiro digito verificar
    multiplicadores_primeiro = list(range(10, 1, -1))
    primeiro_digito =  calcular_digito(cpf, multiplicadores_primeiro)

    # Multiplicadores para o segundo digito verificar
    multiplicadores_segundo = list(range(11, 1, -1))
    segundo_digito = calcular_digito(cpf, multiplicadores_segundo)

    # Verificar se os dígitos calculados são iguais aos informados
    if not (cpf[-2] == str(primeiro_digito) and cpf[-1] == str(segundo_digito)):
        raise ValidationError('CPF inválido')