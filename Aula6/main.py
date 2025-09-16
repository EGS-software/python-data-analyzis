from ContaBanco import ContaBanco

conta1 = ContaBanco(1, "CC", "João Alfredo", 50.0, False, 0)

conta1.abrirConta("CC")
conta1.depositar(100)
conta1.sacar(50)
conta1.taxaMensal(0)
conta1.mostrar()