# Estatísticas básicas - Fase 2 (RM566867)
dados <- read.csv("dadosR.csv", header = TRUE, sep = ",")

print("Visualização dos dados:")
print(head(dados))

media_area   <- mean(dados$Area, na.rm = TRUE)
media_insumo <- mean(dados$InsumoTotal, na.rm = TRUE)
dp_area      <- sd(dados$Area, na.rm = TRUE)
dp_insumo    <- sd(dados$InsumoTotal, na.rm = TRUE)

cat("\n--- Estatísticas Básicas ---\n")
cat("Média da área plantada:", round(media_area, 2), "m²\n")
cat("Desvio padrão da área:", round(dp_area, 2), "m²\n")
cat("Média do total de insumo:", round(media_insumo, 2), "L\n")
cat("Desvio padrão do total de insumo:", round(dp_insumo, 2), "L\n")

resumo <- data.frame(
  Estatistica = c("Media_Area","DP_Area","Media_Insumo","DP_Insumo"),
  Valor = c(media_area, dp_area, media_insumo, dp_insumo)
)
write.csv(resumo, "resumo_estatistico.csv", row.names = FALSE)
print("Resumo salvo em resumo_estatistico.csv")
