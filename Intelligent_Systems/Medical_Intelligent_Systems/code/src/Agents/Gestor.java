package Agents;

import java.io.IOException;
import java.util.HashMap;

import jade.core.AID;
//import Agents.Gestor.Receiver;
import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.core.behaviours.OneShotBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.UnreadableException;
import Classes.Farm;
import Classes.Forn;
import Classes.Position;

public class Gestor extends Agent {
	
	private HashMap<String, Farm> farm_gestor = new HashMap<>();
	private HashMap<String, Forn> forn_gestor = new HashMap<>();
	private int threshold = 2;

	protected void setup() {
		super.setup();
		System.out.print(
				"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@     Starting Gestor     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n");
	
		System.out.print("\n");
		
		addBehaviour(new ContactarFarmacias());
		addBehaviour(new Receiver());
	}
	
	private class ContactarFarmacias extends OneShotBehaviour {
		private static final long serialVersionUID = 1L;
		private int numFarmacias;
		private int numFornecedores;
		
		public void action() {

			try {
				// Contactar todas as farmácias
				DFAgentDescription dfd = new DFAgentDescription();
				ServiceDescription sd = new ServiceDescription();
				sd.setType("Farmacia");
				dfd.addServices(sd);

				DFAgentDescription[] result = DFService.search(this.myAgent, dfd);
				String[] farmacias; //array de AID das farmacias
				farmacias = new String[result.length]; //array de AID das farmacias com tamanho do array result
				numFarmacias = result.length;

				for (int i = 0; i < numFarmacias; ++i) {
					farmacias[i] = result[i].getName().getLocalName(); //introduz no array farmacia o nome de cada farmacia
					
					//envia msg a cada farmacia para ela enviar as suas coordenadas
					ACLMessage mensagem = new ACLMessage(ACLMessage.CFP);
					AID receiver = new AID();
					receiver.setLocalName(farmacias[i]);
					mensagem.addReceiver(receiver);
					myAgent.send(mensagem); 
					}
				
				// Contactar todos os fornecedores
				DFAgentDescription dfd2 = new DFAgentDescription();
				ServiceDescription sd2 = new ServiceDescription();
				sd2.setType("Fornecedor");
				dfd2.addServices(sd2);

				DFAgentDescription[] result2 = DFService.search(this.myAgent, dfd2);
				String[] fornecedores; //array de AID das fornecedores
				fornecedores = new String[result2.length]; //array de AID dos fornecedores com tamanho do array result2
				numFornecedores = result2.length;

				for (int i = 0; i < numFornecedores; ++i) {
					fornecedores[i] = result2[i].getName().getLocalName(); //introduz no array fornecedor o nome de cada fornecedor
					
					//envia msg a cada fornecedor para ela enviar as suas coordenadas
					ACLMessage mensagem2 = new ACLMessage(ACLMessage.CFP);
					AID receiver2 = new AID();
					receiver2.setLocalName(fornecedores[i]);
					mensagem2.addReceiver(receiver2);
					myAgent.send(mensagem2); 
					}
				
				} catch (FIPAException e) {
				e.printStackTrace();
				}			
			}
		}	
	
	private class Receiver extends CyclicBehaviour {
		private static final long serialVersionUID = 1L;
		private String Farmacia;
		private String Pedido;
		private double tempo;
		private String[] med,med1,med2,med3;
		private HashMap<String, Integer> stock;
		private int xFarmacia, yFarmacia, xCidadao, yCidadao;
		private int minDistance = 1000;
		private String cidadaoName;
		private int quantidade;
		AID secondFarmacia = null;
		AID fornecedor_barato = null;
		Forn Forn_mais_barato = null;
		Forn Forn_mais_barato2 = null;
		private String Fornecedor;
		AID Farmacia2 = null;
		int preco = 1000;
		int preco2 = 1000;
		
		public void action() {
			
			ACLMessage msg = receive();
			if (msg != null) {
				
				//Recebe coordenadas de cada farmácia
				if (msg.getPerformative() == ACLMessage.SUBSCRIBE) {
					AID Farmacia2 = msg.getSender();
					Farmacia= msg.getSender().getLocalName();
					
					//Cria uma nova Class_Farmacia guardando no hashmap Farmacias
					try {
						Farm a = (Farm) msg.getContentObject();
						farm_gestor.put(Farmacia,a);

					} catch (UnreadableException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}					
				}
				
				//Recebe coordenadas de cada fornecedor
				else if (msg.getPerformative() == ACLMessage.CFP) {
					try {
						Forn fornecedor = (Forn) msg.getContentObject();
						Fornecedor = msg.getSender().getLocalName();
						forn_gestor.put(Fornecedor,fornecedor);
					} catch (UnreadableException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}					
				}
				
				else if (msg.getPerformative() == ACLMessage.REQUEST) {
					int stock_pedido = 0;
					
					String[] pedido = msg.getContent().split(","); 
					Farmacia =msg.getSender().getLocalName();
					Pedido = pedido[6];
					xCidadao = Integer.parseInt(pedido[2]);
					yCidadao = Integer.parseInt(pedido[3]);
					xFarmacia=Integer.parseInt(pedido[4]);
					yFarmacia=Integer.parseInt(pedido[5]);
					cidadaoName = pedido[1];
					quantidade = Integer.parseInt(pedido[7]);
										
					System.out.println(myAgent.getLocalName() + ": Recebe pedido da " + Farmacia  + " para ver a 2ª Farmácia mais próxima com stock para "
							+ "o produto " + quantidade + " " + Pedido);
					System.out.print("\n");
					
					//Percorre todas as farmácias e escolhe todas à exceção da farmácia sem stock
					for (HashMap.Entry<String, Farm> pair  : farm_gestor.entrySet()) {
						Farm f=pair.getValue();
						if (!f.getAgent().getLocalName().equals(Farmacia)) {
							stock=f.getStock_medicamentos(); //obtem a lista de medicamentos
							xFarmacia = f.getPosition().getX(); 
						    yFarmacia = f.getPosition().getY();
						    
						    //Percorre med2 até encontrar o produto pretendido
							for(HashMap.Entry<String, Integer> med  : stock.entrySet()) {
								if(med.getKey().equals(Pedido)) {
									stock_pedido = med.getValue();//Guarda a quantidade em stock desse mesmo produto
									 									
									//Só calcula a distância se houver stock, caso contrário, avança para a próxima farmácia
									if (stock_pedido>=quantidade) {
										int distance = (int) Math.sqrt(((Math.pow((xCidadao - xFarmacia), 2)) + 
													 (Math.pow((yCidadao - yFarmacia), 2))));
										if (distance < minDistance) {
											minDistance = distance; //altera a distancia minima
											secondFarmacia = f.getAgent();
										}
									}
								}
							}
						}
					}
					//depois de percorrer todas as farmacias, contactar a 2ª mais proxima				
					//Avisa o GESTOR da 2ª farmácia mais próxima 
					
					ACLMessage mensagem = new ACLMessage(ACLMessage.INFORM);
					AID receiver = new AID();
					
					mensagem.addReceiver(secondFarmacia);
					
					System.out.println(myAgent.getLocalName() + ": Avisar a " + secondFarmacia.getLocalName() + " que é a 2ª farmácia mais próxima");
					System.out.print("\n");
					
					mensagem.setContent("Terá de enviar este produto" + "," + Pedido + "," + quantidade + "," + "ao cidadão" + "," + cidadaoName);
					myAgent.send(mensagem); 
									
					minDistance = 1000; //REINICIA A VARIAVEL
					secondFarmacia = null;
					
					//Percorre todos os fornecedores e escolhe o mais barato
					for (HashMap.Entry<String, Forn> pair  : forn_gestor.entrySet()) {
						Forn f=pair.getValue();
						
						int preco_forn=f.buscar_preco_med(Pedido); //obtem a lista de medicamentos
						if (preco_forn < preco) {
							preco = preco_forn;
							Forn_mais_barato = f;
						}						
					}
					
					Farm farma = farm_gestor.get(Farmacia);
					int stock_1farmacia = farma.getStock_medicamentos().get(Pedido);
					int despesa = (9-stock_1farmacia) * Forn_mais_barato.buscar_preco_med(Pedido);
					
					ACLMessage mensagem2 = new ACLMessage(ACLMessage.INFORM);
					AID receiver2 = new AID();
					receiver2 = Forn_mais_barato.getAgent();
					mensagem2.addReceiver(receiver2);
					
					mensagem2.setContent("Terá de enviar este produto" + "," + Pedido + "," + "quantidade" + "," + quantidade + "," + " à farmácia" + "," + Farmacia + "," + despesa);
					myAgent.send(mensagem2);
					
					preco=1000;
					Forn_mais_barato=null;									
				}
				
				else if (msg.getPerformative() == ACLMessage.INFORM_REF) {
					//int preco2 = 1000;
					String[] informacao = msg.getContent().split(",");
					
					String med = informacao[4];
					String ID_Farmacia = informacao[0];
					int quantidade = Integer.parseInt(informacao[6]);
					int quantidade2 = Integer.parseInt(informacao[8]);
					int receita = Integer.parseInt(informacao[2]);
					String customerName= informacao[7];
					Farm Farmacia = farm_gestor.get(ID_Farmacia);
					int vendeu = Farmacia.getStock_medicamentos().get(med) - quantidade;
					//System.out.println(med);
					Farmacia.alterarStock(quantidade, med);
					Farmacia.setReceita(receita);
					Farmacia.setPedidos();
					HashMap<String, Integer> produtos_vendidos= Farmacia.getProdutos_vendidos();
										
					int vendidos = produtos_vendidos.get(med) + vendeu;
					
					produtos_vendidos.put(med, vendidos);
					
					HashMap<String, Integer> farm_cidadao= Farmacia.getCidadaos();
					
					farm_cidadao.put(customerName, quantidade2);
					
					if (quantidade < threshold) {
						//Percorre todas as farmácias e escolhe todas à exceção da farmácia sem stock
						for (HashMap.Entry<String, Forn> pair  : forn_gestor.entrySet()) {
							Forn f=pair.getValue();
							
							int preco_forn=f.buscar_preco_med(med); //obtem a lista de medicamentos
							
							if (preco_forn < preco2) {
								preco2 = preco_forn;
								Forn_mais_barato2 = f;
							}							
						}
						
						int despesa = (9-quantidade) * Forn_mais_barato2.buscar_preco_med(med);
						
						ACLMessage mensagem2 = new ACLMessage(ACLMessage.INFORM);
						AID receiver2 = new AID();
						receiver2 = Forn_mais_barato2.getAgent();
						mensagem2.addReceiver(receiver2);
						
						mensagem2.setContent("Terá de enviar este produto" + "," + med + "," + "quantidade" + "," + quantidade + "," + " à farmácia" + "," +  ID_Farmacia + "," + despesa);
						myAgent.send(mensagem2);
						preco2=1000;
						Forn_mais_barato2=null;
					}
					else {
						 try {
							ACLMessage mensagem = new ACLMessage(ACLMessage.INFORM);
							AID receiver = new AID();
							//int valor = 1;
							receiver.setLocalName("Interface");
							
							System.out.println(myAgent.getLocalName() + ": Avisar a Interface para imprimir resultados!");
							System.out.print("\n");
							
							mensagem.setContentObject(farm_gestor);
							mensagem.addReceiver(receiver);
							myAgent.send(mensagem);
						 }
						 catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}
					}					
				}
				
				else if (msg.getPerformative() == ACLMessage.INFORM) {
					String[] informacao = msg.getContent().split(",");
					
					String med = informacao[2];
					String ID_Farmacia = informacao[0];
					int quantidade = Integer.parseInt(informacao[4]);
					int despesa = Integer.parseInt(informacao[5]);
					
					Farm Farmacia = farm_gestor.get(ID_Farmacia);
					
					HashMap<String, Integer> stock_med = Farmacia.getStock_medicamentos();
					int stock = 10;
					
					Farmacia.alterarStock(9, med);
					Farmacia.setDespesa(despesa);

					try {
						ACLMessage mensagem = new ACLMessage(ACLMessage.INFORM);
						AID receiver = new AID();
						
						receiver.setLocalName("Interface");
						
						System.out.println(myAgent.getLocalName() + ": Avisar a Interface para imprimir resultados!");
						System.out.print("\n");
						
						mensagem.setContentObject(farm_gestor);
						mensagem.addReceiver(receiver);
						myAgent.send(mensagem);
					}
					catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}					
				}				
			}
			else {
				block();
			}
		}
	}
}
