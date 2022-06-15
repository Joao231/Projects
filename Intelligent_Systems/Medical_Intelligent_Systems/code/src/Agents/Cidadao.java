package Agents;

import java.util.ArrayList;
import java.util.Random;

import Classes.Position;
import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.core.behaviours.OneShotBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAException;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.lang.acl.ACLMessage;

public class Cidadao extends Agent {
	private String name;
	int xCidadao, yCidadao; 
	int quantidade;
	int numFarmacias;
	private ArrayList<String> products;
	private String produtoRequisitado;
	private String nome;
	private String nif;
	private String data_nascimento;
	private String morada;
	private String cod_postal;
	
	protected void setup() {
		super.setup();

		System.out.print(
				"********************************************************************************************************************************************************************\n");
		System.out.print(
				"                                                                           Starting Cidadao                                                                         \n");
		System.out.print(
				"********************************************************************************************************************************************************************\n");
		System.out.print("\n");
		
		// As coordenadas do cidadão são escolhidas de forma aleatória
		Random rand = new Random();
		Position init = new Position(rand.nextInt(100), rand.nextInt(100));
		xCidadao= init.getX();
		yCidadao = init.getY();
		products = new ArrayList<String>();
		
		products.add("brufen");
		products.add("ben-u-ron");
		products.add("aspirina");
		products.add("xanax");
		products.add("valium");
		products.add("fenistil");
		products.add("voltaren");
		products.add("buscopan");
		products.add("leite NAN");
		products.add("kompensan");
		products.add("rennie");
		products.add("bissolvon");
		products.add("strepfen");
	
		
		produtoRequisitado = "";
		this.addBehaviour(new Apresentacao());
		this.addBehaviour(new ContactarFarmacias());
		this.addBehaviour(new Receiver());
	}
	
	private class Apresentacao extends OneShotBehaviour {
		public void action() {
			char aChar = myAgent.getLocalName().charAt(myAgent.getLocalName().length() - 1);
			
			if (aChar=='0') {
				nome = "Joao Alves";
				nif = "123456789";
				data_nascimento = "18/02/2000";
				morada = "Rua dos Santos, Braga";
				cod_postal = "4730-465";
			}
			if (aChar=='1') {
				nome = "Paulo Alves";
				nif = "126435689";
				data_nascimento = "26/07/1980";
				morada = "Rua dos Barbaros, Porto";
				cod_postal = "4820-465";
			}
			if (aChar=='2') {
				nome = "Rodrigo Cardoso";
				nif = "222226789";
				data_nascimento = "18/09/1998";
				morada = "Rua dos Anjos, Coimbra";
				cod_postal = "4900-333";
			}
			if (aChar=='3') {
				nome = "Marta Pereira";
				nif = "123453421";
				data_nascimento = "20/02/1990";
				morada = "Rua dos Pepinos, Lisboa";
				cod_postal = "4875-455";
			}
			if (aChar=='4') {
				nome = "Jose Marco";
				nif = "132323789";
				data_nascimento = "21/05/2000";
				morada = "Rua dos Morcegos, Braga";
				cod_postal = "4500-440";
			}
			if (aChar=='5') {
				nome = "Antonio dos Anjos";
				nif = "987654321";
				data_nascimento = "23/07/2010";
				morada = "Rua das Santas, Porto";
				cod_postal = "4900-444";
			}
			if (aChar=='6') {
				nome = "Manuel Rogério";
				nif = "465738291";
				data_nascimento = "10/01/1970";
				morada = "Rua dos Macacos, Braga";
				cod_postal = "4910-432";
			}
			if (aChar=='7') {
				nome = "Jorge Tiago";
				nif = "965496786";
				data_nascimento = "29/10/2005";
				morada = "Rua dos Raios, Porto";
				cod_postal = "4730-478";
			}
			if (aChar=='8') {
				nome = "Ana Goncalves";
				nif = "254722777";
				data_nascimento = "30/04/2001";
				morada = "Rua dos Felizes, Lisboa";
				cod_postal = "4810-465";
			}
			if (aChar=='9') {
				nome = "Sofia Marbella";
				nif = "123876987";
				data_nascimento = "12/02/1988";
				morada = "Rua dos Tristes, Lisboa";
				cod_postal = "4720-323";
			}
			
			System.out.println("Olá eu sou o " + myAgent.getLocalName());
			
			System.out.println("\n");
			
			System.out.println("Nome: " + nome);
			System.out.println("NIF: " + nif);
			System.out.println("Data nascimento: " + data_nascimento);
			System.out.println("Morada: " + morada);
			System.out.println("Codigo-Postal: " + cod_postal);
			
			System.out.println("\n");
		}
	}
	
	private class ContactarFarmacias extends OneShotBehaviour {
		public void action() {

			try {
				// Contactar todas as farmácias
				DFAgentDescription dfd = new DFAgentDescription();
				ServiceDescription sd = new ServiceDescription();
				sd.setType("Farmacia");
				dfd.addServices(sd);

				DFAgentDescription[] result = DFService.search(this.myAgent, dfd);
				
				if (result.length > 0) {
					for (int i = 0; i < result.length; ++i) {
						// Agent Found
						DFAgentDescription dfd1 = result[i];
						AID provider = new AID();
						provider.setLocalName(dfd1.getName().getLocalName());
						numFarmacias = result.length;
					
						//Envia msg a cada uma para pedir as suas coordenadas
						ACLMessage mensagem = new ACLMessage(ACLMessage.SUBSCRIBE);
						mensagem.addReceiver(provider);
						myAgent.send(mensagem);
					}
				}				
			}			
				catch (FIPAException fe) {
					fe.printStackTrace();
				}
			}
		}
	
	private class Receiver extends CyclicBehaviour {
		private int xOrigin, yOrigin;
		private int minDistance = 1000;
		private String closestFarmacia; //farmacia mais proxima
		private int FarmaciasProcessadas = 0;

		@Override
		public void action() {
			ACLMessage msg = receive();
			name = myAgent.getLocalName();
			if (msg != null) {
				//Recebe msg da farmacia
				if (msg.getPerformative() == ACLMessage.INFORM) { // RECEBE COORDENADAS 
					String[] coordinates = msg.getContent().split(","); //Separa as coordenadas e atribui o valor às variáveis definidas inicialmente
					FarmaciasProcessadas++; 
					xOrigin = Integer.parseInt(coordinates[0]);
					yOrigin = Integer.parseInt(coordinates[1]);
					
					// Calcula a distancia entre o cidadão e cada farmácia
					int distance = (int) Math
							.sqrt(((Math.pow((xCidadao - xOrigin), 2)) + (Math.pow((yCidadao - yOrigin), 2))));
						
					if (distance < minDistance) {
						minDistance = distance; //altera a distancia minima
						closestFarmacia = msg.getSender().getLocalName(); //altera a farmacia + proxima
					}
					if (FarmaciasProcessadas == numFarmacias) { //se já processei todas as farmacias
							
						Random randomizer = new Random(); 
						String random = products.get(randomizer.nextInt(products.size())); // Escolhe um produto random da lista
						produtoRequisitado = random;
						Random rand = new Random();
						while (true) {
							quantidade = rand.nextInt(10);
							if (quantidade !=0) {
								break;
							}
						}
						
						//DESCOMENTADO APENAS PARA DEMONSTRAÇÃO
						//closestFarmacia="Farmacia0";
						//produtoRequisitado="rennie";
						
						System.out.println(name + ": Escolheu a " + closestFarmacia + " pedindo: " + quantidade + " " + produtoRequisitado);
						System.out.print("\n");
						
						ACLMessage mensagem = new ACLMessage(ACLMessage.REQUEST); //envia msg a farmacia para fazer o pedido 
						AID receiver = new AID();
						receiver.setLocalName(closestFarmacia);
						mensagem.addReceiver(receiver);
						mensagem.setContent("Cidadao:" + "," + xCidadao + "," + yCidadao + "," + produtoRequisitado + ","+ quantidade );
						myAgent.send(mensagem);
						FarmaciasProcessadas = 0; //reinicia as variaveis
						minDistance = 1000;
						closestFarmacia = null;
						}
				}
				
				else if (msg.getPerformative() == ACLMessage.AGREE) {
					name = myAgent.getLocalName();
					System.out.println(name + ": Recebi o meu pedido. Obrigado!" + msg.getSender().getLocalName());
					System.out.print("\n");
					myAgent.doDelete();
				}
			}				
		}
	}
	
	protected void takeDown() {
		System.out.println("Ending Customer");
		super.takeDown();
	}
	
}