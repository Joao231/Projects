package Classes;

import java.util.HashMap;

import jade.core.AID;

public class Farm implements java.io.Serializable{
	
	private AID agent;
	private Position position;
	private HashMap<String, Integer> stock_medicamentos = new HashMap<>();
	private HashMap<String, Integer> preco_medicamentos = new HashMap<>();
	private HashMap<String, Integer> produtos_vendidos = new HashMap<>();
	private HashMap<String, Integer> farm_cidadao = new HashMap<>();
	int receita;
	int despesa;
	int pedidos;
	
	public Farm(AID agent, Position position) {
		
		this.agent = agent;
		this.position = position;
			
		stock_medicamentos.put("brufen", 9); stock_medicamentos.put("ben-u-ron", 9); stock_medicamentos.put("aspirina", 9); stock_medicamentos.put("xanax", 9);
		stock_medicamentos.put("valium", 9); stock_medicamentos.put("fenistil", 9); stock_medicamentos.put("voltaren", 9); stock_medicamentos.put("buscopan", 9);
		stock_medicamentos.put("leite NAN", 9);stock_medicamentos.put("kompensan", 9);stock_medicamentos.put("rennie", 9);stock_medicamentos.put("bissolvon", 9);
		stock_medicamentos.put("strepfen", 9);
		
		preco_medicamentos.put("brufen", 10); preco_medicamentos.put("ben-u-ron", 12); preco_medicamentos.put("aspirina", 8); preco_medicamentos.put("xanax", 10);
		preco_medicamentos.put("valium", 11); preco_medicamentos.put("fenistil", 15); preco_medicamentos.put("voltaren", 13); preco_medicamentos.put("buscopan", 8);
		preco_medicamentos.put("leite NAN", 10);preco_medicamentos.put("kompensan", 10);preco_medicamentos.put("rennie", 15);preco_medicamentos.put("bissolvon", 10);
		preco_medicamentos.put("strepfen", 12);
			
		produtos_vendidos.put("brufen", 0); produtos_vendidos.put("ben-u-ron", 0); produtos_vendidos.put("aspirina", 0); produtos_vendidos.put("xanax", 0);
		produtos_vendidos.put("valium", 0); produtos_vendidos.put("fenistil", 0); produtos_vendidos.put("voltaren", 0); produtos_vendidos.put("buscopan", 0);
		produtos_vendidos.put("leite NAN", 0);produtos_vendidos.put("kompensan", 0);produtos_vendidos.put("rennie", 0);produtos_vendidos.put("bissolvon", 0);
		produtos_vendidos.put("strepfen", 0);
			
		farm_cidadao.put("Cidadao0", 0); farm_cidadao.put("Cidadao1", 0); farm_cidadao.put("Cidadao2", 0); farm_cidadao.put("Cidadao3", 0);
		farm_cidadao.put("Cidadao4", 0); farm_cidadao.put("Cidadao5", 0); farm_cidadao.put("Cidadao6", 0); farm_cidadao.put("Cidadao7", 0);
		farm_cidadao.put("Cidadao8", 0);farm_cidadao.put("Cidadao9", 0);
		
		receita=0;
		despesa=0;
		pedidos=0;
	}
	
	public HashMap<String, Integer> getCidadaos() {
		return farm_cidadao;
	}

	public void setCidadaos(HashMap<String, Integer> farm_cidadao) {
		this.farm_cidadao = farm_cidadao;
	}
	
	public HashMap<String, Integer> getPreco_medicamentos() {
		return preco_medicamentos;
	}

	public void setPreco_medicamentos(HashMap<String, Integer> preco_medicamentos) {
		this.preco_medicamentos = preco_medicamentos;
	}
	
	public int getReceita() {
		return receita;
	}

	public void setReceita(int valor) {
		this.receita += valor;
	}
	
	public int getDespesa() {
		return despesa;
	}

	public void setDespesa(int valor) {
		this.despesa += valor;
	}

	public int getPedidos() {
		return pedidos;
	}

	public void setPedidos() {
		this.pedidos += 1;
	}
	
	public Position getPosition() {
		return position;
	}
	
	public void setPosition(Position position) {
		this.position = position;
	}
	
	public AID getAgent() {
		return agent;
	}
	
	public HashMap<String, Integer> getProdutos_vendidos() {
		return produtos_vendidos;
	}
	
	public void setProdutosVendidos(HashMap<String, Integer> produtos_vendidos) {
		this.produtos_vendidos = produtos_vendidos;
	}
	
	public HashMap<String, Integer> getStock_medicamentos() {
		return stock_medicamentos;
	}
	
	public void setStock_medicamentos(HashMap<String, Integer> stock_medicamentos) {
		this.stock_medicamentos = stock_medicamentos;
	}
	
	public void alterarStock(int stock, String medicamento){
		   stock_medicamentos.put(medicamento, stock);
	}	
	
	public void alterarVendido(int quantidade, String medicamento){
		   produtos_vendidos.put(medicamento, quantidade);
	}	
}
