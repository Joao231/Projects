import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.core.Runtime;
import jade.wrapper.AgentController;
import jade.wrapper.ContainerController;

public class MainContainer {

	Runtime rt;
	ContainerController container;

	public static void main(String[] args) {
		MainContainer a = new MainContainer();

		a.initMainContainerInPlatform("localhost", "9888", "MainContainer");
	
		int n;
		int limit_farmacias = 6; 
		int limit_cidadaos = 10;
		int limit_fornecedores = 2;

		// Start Agents Farmacias!
		for (n = 0; n < limit_farmacias; n++) {
			try {
				a.startAgentInPlatform("Farmacia" + n, "Agents.Farmacia");
				Thread.sleep(500);
			
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		
			try {
				Thread.sleep(500);
			} catch (InterruptedException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		
		// Start Agents Fornecedores!
		for (n = 0; n < limit_fornecedores; n++) {
			try {
				a.startAgentInPlatform("Fornecedor" + n, "Agents.Fornecedor");
				Thread.sleep(500);
			
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		
			try {
				Thread.sleep(500);
			} catch (InterruptedException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
					
		try {
			a.startAgentInPlatform("Gestor", "Agents.Gestor");
			Thread.sleep(500);
		} catch (InterruptedException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
						
		try {
			a.startAgentInPlatform("Interface", "Agents.Interface");
			Thread.sleep(500);
		}
			catch (InterruptedException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		
		// Start Agents Cidadaos!
		for (n = 0; n < limit_cidadaos; n++) {
			try {
				a.startAgentInPlatform("Cidadao" + n, "Agents.Cidadao");
				Thread.sleep(5000);
			}
			catch (InterruptedException e) {
			e.printStackTrace();
			}
		}
		
	}

	public ContainerController initContainerInPlatform(String host, String port, String containerName) {
		// Get the JADE runtime interface (singleton)
		this.rt = Runtime.instance();

		// Create a Profile, where the launch arguments are stored
		Profile profile = new ProfileImpl();
		profile.setParameter(Profile.CONTAINER_NAME, containerName);
		profile.setParameter(Profile.MAIN_HOST, host);
		profile.setParameter(Profile.MAIN_PORT, port);
		// create a non-main agent container
		ContainerController container = rt.createAgentContainer(profile);
		return container;
	}

	public void initMainContainerInPlatform(String host, String port, String containerName) {

		// Get the JADE runtime interface (singleton)
		this.rt = Runtime.instance();

		// Create a Profile, where the launch arguments are stored
		Profile prof = new ProfileImpl();
		prof.setParameter(Profile.CONTAINER_NAME, containerName);
		prof.setParameter(Profile.MAIN_HOST, host);
		prof.setParameter(Profile.MAIN_PORT, port);
		prof.setParameter(Profile.MAIN, "true");
		prof.setParameter(Profile.GUI, "true");

		// create a main agent container
		this.container = rt.createMainContainer(prof);
		rt.setCloseVM(true);
	}

	public void startAgentInPlatform(String name, String classpath) {
		try {
			AgentController ac = container.createNewAgent(name, classpath, new Object[0]);
			ac.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
