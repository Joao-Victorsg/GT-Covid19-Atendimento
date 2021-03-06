"""Adição de views ao banco

Revision ID: 1e6edc8baee8
Revises: 8b737f85bd67
Create Date: 2020-08-24 17:43:33.654080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e6edc8baee8'
down_revision = '8b737f85bd67'
branch_labels = None
depends_on = None

def upgrade():

    op.execute(
        "create view vw_atendimentos_relacoes as \
         select atendimentos.data as data,\
            atendimentos.id_paciente,\
            atendimentos_relacao.data_sintomas as data_primeiro_sintoma,\
            atendimentos_relacao.dosagem       as dosagem,\
            doencas_cronicas.value             as doenca_cronica,\
            parentescos.value                  as parentesco,\
            indicadores.value                  as indicador,\
            sintomas.value                     as sintoma \
        from parentescos, atendimentos_relacao \
                left join atendimentos\
                        on atendimentos_relacao.id_atendimento = atendimentos.id\
                left join doencas_cronicas\
                        on atendimentos_relacao.id_doenca_cronica = doencas_cronicas.id\
                left join indicadores\
                        on atendimentos_relacao.id_indicador = indicadores.id\
                left join sintomas\
                        on atendimentos_relacao.id_sintoma = sintomas.id \
        where atendimentos_relacao.id_parentesco = parentescos.id;"
    )

    op.execute(
        "create view vw_atendimentos_sintoma_pessoa as \
         select atendimentos.data as data,\
            atendimentos.id_paciente,\
            atendimentos_relacao.data_sintomas as data_primeiro_sintoma,\
            atendimentos_relacao.dosagem       as dosagem,\
            indicadores.value                  as indicador,\
            sintomas.value                     as sintoma \
        from atendimentos_relacao\
                left join atendimentos\
                        on atendimentos_relacao.id_atendimento = atendimentos.id\
                left join indicadores\
                        on atendimentos_relacao.id_indicador = indicadores.id\
                left join sintomas\
                        on atendimentos_relacao.id_sintoma = sintomas.id;"
    )

    op.execute(
        "create view vw_atendimentos_visitas as \
         select\
            atendimentos.data as data,\
            atendimentos.id_paciente,\
            atendimentos_visitas.quem_visitou as quem_visitou,\
            atendimentos_visitas.porque_visitou as porque_visitou\
        from\
            atendimentos_visitas\
            left join atendimentos on\
                atendimentos_visitas.id_atendimento = atendimentos.id;"
    )

    op.execute(
        "create view  vw_atendimentos_motivos_sair as \
         select\
            atendimentos.data as data,\
            atendimentos.id_paciente,\
            atendimentos_motivos_sair.id,\
            atendimentos_motivos_sair.outros_motivos_sair as outros,\
            motivos_sair.value as motivo_sair \
        from \
            atendimentos_motivos_sair\
            left join atendimentos\
                on atendimentos_motivos_sair.id_atendimento = atendimentos.id\
            left join motivos_sair\
                on atendimentos_motivos_sair.id_motivo_sair = motivos_sair.id;"
    )

    op.execute(
        "create view vw_atendimentos_beneficios_sociais as \
         select\
            atendimentos.data as data,\
            atendimentos.id_paciente,\
            atendimentos_beneficios_sociais.id,\
            atendimentos_beneficios_sociais.outros_beneficios_sociais as outros,\
            beneficios_sociais.value as beneficios_sociais \
        from\
            atendimentos_beneficios_sociais\
            left join atendimentos on\
                atendimentos_beneficios_sociais.id_atendimento = atendimentos.id\
            left join beneficios_sociais\
                on atendimentos_beneficios_sociais.id_beneficio_social = beneficios_sociais.id;"
    )

    op.execute(
        "create view vw_atendimentos_estrategias_saudes_familiar as \
         select\
            atendimentos_estrategias_saudes_familiar.id,\
            atendimentos_estrategias_saudes_familiar.outras_estrategias_saude_familiar as outros,\
            estrategias_saude_familiar.value as estrategias_saude_familiar,\
            atendimentos.data as data,\
            atendimentos.id_paciente as id_paciente \
        from\
            atendimentos_estrategias_saudes_familiar\
                left join atendimentos\
                    on atendimentos_estrategias_saudes_familiar.id_atendimento = atendimentos.id\
                left join estrategias_saude_familiar\
                    on atendimentos_estrategias_saudes_familiar.id_estrategia_saude_familiar = estrategias_saude_familiar.id;"
    )

    op.execute(
        "create view vw_atendimentos_orientacoes_finais as \
         select\
            a.data as data,\
            a.id_paciente,\
            atendimentos_orientacoes_finais.outras_orientacoes_finais as outras,\
            atendimentos_orientacoes_finais.comentario as comentario,\
            orientacoes_finais.value \
        from\
            atendimentos_orientacoes_finais\
            left join atendimentos a\
                on atendimentos_orientacoes_finais.id_atendimento = a.id\
            left join orientacoes_finais\
                on atendimentos_orientacoes_finais.id_orientacao_final = orientacoes_finais.id;"
    )



def downgrade():
    op.execute("drop view if exists vw_atendimentos_relacoes;")
    op.execute("drop view if exists vw_atendimentos_sintoma_pessoa;")
    op.execute("drop view if exists vw_atendimentos_visitas;")
    op.execute("drop view if exists vw_atendimentos_motivos_sair;")
    op.execute("drop view if exists vw_atendimentos_beneficios_sociais;")
    op.execute("drop view if exists vw_atendimentos_estrategias_saudes_familiar;")
    op.execute("drop view if exists vw_atendimentos_orientacoes_finais;")
