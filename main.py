from labirinto.labirinto import Labirinto

if __name__ == '__main__':
    lab = Labirinto(
        dim_x=10,
        dim_y=10,
        taxa_obstaculos=.2
    )
    # lab.imprimir_labirinto()
    lab.desenha_labirinto()

    # print(lab.faz_busca_em_largura(print_map=True))
    print(lab.faz_busca_com_informacao())
