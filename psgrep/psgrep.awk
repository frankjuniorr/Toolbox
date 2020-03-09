BEGIN{
  printf "%s\t%s\t%s\t%s\t%s\n", "USER","PID","%CPU", "%MEM", "COMMAND"
}

{
  # esse bloco imprime um separador (****) pra cada linha do resultado da busca dos processos
  out=""
  for(i=1;i<=NF;i++){
    out=$out
  }
  print $out
  print "**********************************"
}