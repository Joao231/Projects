package Agents;

import java.io.IOException;
import java.io.Serializable;
import java.util.HashMap;
import java.util.Random;

import Classes.Farm;
import Classes.Position;
import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.lang.acl.ACLMessage;

public class Farmacia extends Agent {

	int xFarmacia, yFarmacia;
	
	private HashMap<String, Integer> stock_medicamentos = new HashMap<>();
	private HashMap<String, Integer> preco_medicamentos = new HashMap<>();
	
	private Farm farmacia;
	
	protected void setup() {
		super.setup();
		
		System.out.print(
				"--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");
		
		System.out.print(
				"                                                                            Starting Farmacia                                                                      \n");
			
		System.out.print(
				"--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");
				
		System.out.print("\n");
		
		// As coordenadas da farmácia são escolhidas de forma aleatória
		Random rand = new Random();
		
		xFarmacia = rand.nextInt(100);
		yFarmacia = rand.nextInt(100);
		
		Position init = new Position(xFarmacia, yFarmacia);
		
		stock_medicamentos.put("brufen", 9); stock_medicamentos.put("ben-u-ron", 9); stock_medicamentos.put("aspirina", 9); stock_medicamentos.put("xanax", 9);
		stock_medicamentos.put("valium", 9); stock_medicamentos.put("fenistil", 9); stock_medicamentos.put("voltaren", 9); stock_medicamentos.put("buscopan", 9);
		stock_medicamentos.put("leite NAN", 9);stock_medicamentos.put("kompensan", 9);stock_medicamentos.put("rennie", 9);stock_medicamentos.put("bissolvon", 9);
		stock_medicamentos.put("strepfen", 9);
		
		preco_medicamentos.put("brufen", 10); preco_medicamentos.put("ben-u-ron", 12); preco_medicamentos.put("aspirina", 8); preco_medicamentos.put("xanax", 10);
		preco_medicamentos.put("valium", 11); preco_medicamentos.put("fenistil", 15); preco_medicamentos.put("voltaren", 13); preco_medicamentos.put("buscopan", 8);
		preco_medicamentos.put("leite NAN", 10);preco_medicamentos.put("kompensan", 10);preco_medicamentos.put("rennie", 15);preco_medicamentos.put("bissolvon", 10);
		preco_medicamentos.put("strepfen", 12);

		// Cada farmácia regista-se nas páginas amarelas
		DFAgentDescription dfd = new DFAgentDescription();
		dfd.setName(getAID());
		ServiceDescription sd = new ServiceDescription();
		sd.setType("Farmacia");
		sd.setName(getLocalName());
		dfd.addServices(sd);
		
		try {
			DFService.register(this, dfd);
		} catch (FIPAException fe) {
			fe.printStackTrace();
		}

		//Comportamento
		addBehaviour(new Receiver());
	}
	
	
private class Receiver extends CyclicBehaviour { 
		
		private int xCidadao, yCidadao;
		private String Pedido;
		private int quantidade;
		private String customerName;
		
		public void action() {
			ACLMessage msg = receive();
			if (msg != null) {
				//Recebe msg do cidadao e envia-lhe as suas coordenadas 
				if (msg.getPerformative() == ACLMessage.SUBSCRIBE) {
				
					System.out.println(myAgent.getLocalName() + ": Recebi pedido do " + msg.getSender().getLocalName() + 
							" para enviar as minhas coordenadas");
					System.out.print("\n");
					
					AID provider = msg.getSender();
					ACLMessage response = new ACLMessage(ACLMessage.INFORM); //responde à msg do cidadao mas agora no tipo INFORM
					response.addReceiver(provider);
					response.setContent(xFarmacia + "," + yFarmacia); //envia as suas coordenadas
					myAgent.send(response);
				}
				
				//Recebe msg do gestor e envia-lhe as suas coordenadas 
				else if (msg.getPerformative() == ACLMessage.CFP) {
										
					try {
						System.out.println(myAgent.getLocalName() + ": Recebi pedido do Gestor para enviar as minhas informacoes");
						System.out.print("\n");
							
						Random rand = new Random();
						farmacia = new Farm(myAgent.getAID(),
								new Position(xFarmacia, yFarmacia));
						
						ACLMessage mensagem = new ACLMessage(ACLMessage.SUBSCRIBE);
						mensagem.setContentObject(farmacia);
						
						mensagem.addReceiver(msg.getSender());

						myAgent.send(mensagem);
						
						}					
						
						catch (IOException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}					
				}
				
				//Recebe msg da interface e envia-lhe as suas coordenadas
				else if (msg.getPerformative() == ACLMessage.PROPOSE) {
					try {
						System.out.println(myAgent.getLocalName() + ": Recebi pedido da Interface para enviar as minhas informacoes");
						System.out.print("\n");
									
						Random rand = new Random();
						farmacia = new Farm(myAgent.getAID(),
								new Position(xFarmacia, yFarmacia));
						
						ACLMessage mensagem = new ACLMessage(ACLMessage.SUBSCRIBE);
						mensagem.setContentObject(farmacia);
							
						mensagem.addReceiver(msg.getSender());
				
						myAgent.send(mensagem);
					}
					catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
				else if (msg.getPerformative() == ACLMessage.REQUEST) {
					String[] Pedido_Coordenadas = msg.getContent().split(","); //Separa as coordenadas do cidadao e atribui o valor às variáveis definidas inicialmente
					xCidadao = Integer.parseInt(Pedido_Coordenadas[1]);
					yCidadao = Integer.parseInt(Pedido_Coordenadas[2]);
					Pedido = Pedido_Coordenadas[3];
					quantidade = Integer.parseInt(Pedido_Coordenadas[4]);
					customerName = msg.getSender().getLocalName();
										
					if (stock_medicamentos.get(Pedido) >=quantidade) {
						//Confirma o pedido ao cidadao
						
						System.out.println(myAgent.getLocalName() + ": Confirma o pedido ao " + customerName);
						System.out.print("\n");
											
						//Adormece durante 0.5 segundos para simular o tempo de entrega 
						try {
							Thread.sleep(500);
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
						
						//E avisa o cidadão que o seu pedido foi entregue
						AID receiver = new AID();
						receiver.setLocalName(customerName);
						ACLMessage mensagem = new ACLMessage(ACLMessage.AGREE);
						mensagem.addReceiver(receiver);
						mensagem.setContent("O seu pedido foi entregue!");
						myAgent.send(mensagem);
						
						int stock = stock_medicamentos.get(Pedido);
						
						int left = stock - quantidade;
						
						stock_medicamentos.put(Pedido, left);
						
						int preco = preco_medicamentos.get(Pedido);
						
						int receita = preco * quantidade;						
						
						AID receiver2 = new AID();
						receiver2.setLocalName("Gestor");
						ACLMessage mensagem2 = new ACLMessage(ACLMessage.INFORM_REF);
						mensagem2.setContent(myAgent.getLocalName() + "," + "aumentar 1 unidade pedidos e aumentar receita para"+ "," + receita + "," + "atualizei stock:" + "," + Pedido +"," + "para" + "," + left + "," + customerName +"," + quantidade);
						mensagem2.addReceiver(receiver2);

						System.out.println(myAgent.getLocalName() + ": Envia de informação de atualização de stock ao Gestor");
						System.out.print("\n");
						
						myAgent.send(mensagem2);
					}
					else {						
						System.out.println(myAgent.getLocalName() + ": Pede ao Gestor a 2ª farmácia mais próxima");
						System.out.print("\n");
						//Envia pedido ao Gestor para ele verificar o stock
						AID receiver = new AID();
						receiver.setLocalName("Gestor");
						ACLMessage mensagem = new ACLMessage(ACLMessage.REQUEST);
						mensagem.setContent(myAgent.getLocalName() + " nao tenho stock para este pedido:" + ","+  customerName + "," + xCidadao + "," + yCidadao + "," + xFarmacia + "," + yFarmacia + "," + Pedido + "," + quantidade);
						mensagem.addReceiver(receiver);
	
						System.out.println(myAgent.getLocalName() + ": Envia pedido ao Gestor");
						System.out.print("\n");
						
						myAgent.send(mensagem);
					}
				}
				else if (msg.getPerformative() == ACLMessage.INFORM) {
					String[] informacao = msg.getContent().split(",");
					
					String pedido = informacao[1];
					int quantidade = Integer.parseInt(informacao[2]);
					String cidadao_name = informacao[4];
					
					System.out.println(myAgent.getLocalName() + ": Confirma o pedido ao " + cidadao_name);
					System.out.print("\n");
				
					ACLMessage resp = msg.createReply();
					resp.setPerformative(ACLMessage.CONFIRM);
					resp.setContent("FARMACIA: Confirma ao cidadão o seu pedido para o produto" + "," + pedido + quantidade);
					System.out.print("\n");
					
					//Adormece durante 0.5 segundos para simular o tempo de entrega 
					try {
						Thread.sleep(500);
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					
					//E avisa o cidadão que o seu pedido foi entregue
					AID receiver = new AID();
					receiver.setLocalName(cidadao_name);
					ACLMessage mensagem = new ACLMessage(ACLMessage.AGREE);
					mensagem.addReceiver(receiver);
					mensagem.setContent("O seu pedido foi entregue!");
					myAgent.send(mensagem);
										
					int stock = stock_medicamentos.get(pedido);
					
					int left = stock - quantidade;
					
					stock_medicamentos.put(pedido, left);
					
					int preco = preco_medicamentos.get(pedido);
					
					int preco_total = preco * quantidade;
					
					AID receiver2 = new AID();
					receiver2.setLocalName("Gestor");
					ACLMessage mensagem2 = new ACLMessage(ACLMessage.INFORM_REF);
					mensagem2.setContent(myAgent.getLocalName() + "," + "aumentar 1 unidade pedidos e aumentar lucro para"+ "," + preco_total + "," + "atualizei stock:" + "," + pedido +"," + "para" + "," + left + "," + cidadao_name + "," + quantidade);
					mensagem2.addReceiver(receiver2);

					System.out.println(myAgent.getLocalName() + ": Envia de informação de atualização de stock ao Gestor");
					System.out.print("\n");
					
					myAgent.send(mensagem2);					
				}				

				else if (msg.getPerformative() == ACLMessage.INFORM_IF) {
					
					System.out.println(myAgent.getLocalName() + ": Recebi o lote que precisava. Obrigado! " + msg.getSender().getLocalName());
					System.out.print("\n");
					
					String[] informacao = msg.getContent().split(",");
					
					String med = informacao[1];
					String ID_Farmacia = informacao[3];
					int despesa = Integer.parseInt(informacao[5]);
									
					stock_medicamentos.put(med, 9);
					
					int quantidade = 9;
					
					AID receiver = new AID();
					receiver.setLocalName("Gestor");
					ACLMessage mensagem = new ACLMessage(ACLMessage.INFORM);
					mensagem.setContent(myAgent.getLocalName() + "," + "atualizei stock:" + "," + med +"," + "para " + "," + quantidade + "," + despesa);
					mensagem.addReceiver(receiver);

					System.out.println(myAgent.getLocalName() + ": Envia de informação de atualização de stock ao Gestor");
					System.out.print("\n");
					
					myAgent.send(mensagem);					
				}
			}
			else {
				block();
			}
		}
	}	
}
