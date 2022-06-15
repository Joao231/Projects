package Agents;

import java.io.IOException;
import java.util.HashMap;
import java.util.Random;

import Classes.Forn;
import Classes.Position;
import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.lang.acl.ACLMessage;

public class Fornecedor extends Agent {
	private HashMap<String, Integer> med_prec = new HashMap<>();

	protected void setup() {
		super.setup();
		
		System.out.print(
				"--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");
		
		System.out.print(
				"                                                                            Starting Fornecedor                                                                      \n");
			
		System.out.print(
				"--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n");
			
		System.out.print("\n");
		
		// Cada fornecedor regista-se nas páginas amarelas
		DFAgentDescription dfd = new DFAgentDescription();
		dfd.setName(getAID());
		ServiceDescription sd = new ServiceDescription();
		sd.setType("Fornecedor");
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
		
		public void action() {
			ACLMessage msg = receive();
			if (msg != null) {
				//Recebe msg do gestor e envia-lhe as suas coordenadas 
				if (msg.getPerformative() == ACLMessage.CFP) {					
					
					try {
						System.out.println(myAgent.getLocalName() + ": Recebi pedido do Gestor para enviar as minhas informacoes");
						System.out.print("\n");
			
						char aChar = myAgent.getLocalName().charAt(10);
						//System.out.println(aChar=='0');
						if (aChar=='0') {
							med_prec.put("brufen", 5); med_prec.put("ben-u-ron", 6); med_prec.put("aspirina", 7); med_prec.put("xanax", 8);
							med_prec.put("valium", 9); med_prec.put("fenistil", 10); med_prec.put("voltaren", 5); med_prec.put("buscopan", 6);
							med_prec.put("leite NAN", 7);med_prec.put("kompensan", 8);med_prec.put("rennie", 11);med_prec.put("bissolvon", 7);
							med_prec.put("strepfen", 9);
						}
						
						if (aChar=='1') {
							med_prec.put("brufen", 9); med_prec.put("ben-u-ron", 10); med_prec.put("aspirina", 3); med_prec.put("xanax", 5);
							med_prec.put("valium", 7); med_prec.put("fenistil", 6); med_prec.put("voltaren", 9); med_prec.put("buscopan", 5);
							med_prec.put("leite NAN", 8);med_prec.put("kompensan", 7);med_prec.put("rennie", 7);med_prec.put("bissolvon", 9);
							med_prec.put("strepfen", 10);
						}
												
						Forn fornecedor = new Forn(myAgent.getAID());
						fornecedor.setSMed_preco(med_prec);
						ACLMessage mensagem = new ACLMessage(ACLMessage.CFP);
						mensagem.setContentObject(fornecedor);
									
						mensagem.addReceiver(msg.getSender());
						
						myAgent.send(mensagem);
						}
									
						catch (IOException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
				}
				if (msg.getPerformative() == ACLMessage.INFORM) { 
					
					String[] pedido = msg.getContent().split(","); 
					String ID_Farmacia = pedido[5];
					String Pedido = pedido[1];
					String quantidade = pedido[3];
					int depesa = Integer.parseInt(pedido[6]);
								
					System.out.println(myAgent.getLocalName() + ": Recebe pedido do GESTOR para reestabelecer o stock na " +
					ID_Farmacia + " para o produto " + Pedido);
					System.out.print("\n");
					
					//Adormece durante 0.5 segundos para simular o tempo de entrega 
					try {
						Thread.sleep(500);
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					
					//Avisa farmácia para reestabelecer o stock
					AID receiver_2 = new AID();
					receiver_2.setLocalName(ID_Farmacia);
					ACLMessage mensagem_2 = new ACLMessage(ACLMessage.INFORM_IF);
					mensagem_2.addReceiver(receiver_2);
					mensagem_2.setContent("O stock para o medicamento" + "," + Pedido + "," +
					"para a farmácia" + "," + ID_Farmacia + "," + "tem que ser reestabelecido para 9" + "," + depesa);
					myAgent.send(mensagem_2);
				}
			}			
		}	
	}	
}
