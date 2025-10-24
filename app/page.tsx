import ChatContainer from "@/components/ChatContainer";
import GraphOne from "@/components/GraphOne";
import GraphTwo from "@/components/GraphTwo";
import GraphThree from "@/components/GraphThree";
import GraphFour from "@/components/GraphFour";
import GraphFive from "@/components/GraphFive";
import State from "@/components/State";

export default function Home() {
	return (
		<main className=" text-indigo-dye-100 font-medium relative min-h-screen w-screen">
			<div className="absolute top-5 left-5 text-2xl font-black text-emerald-400 z-50">
				TANI.iO
			</div>
			<div className="flex flex-row justify-center items-start w-screen h-screen pt-16 px-4 gap-2	">
				<div className="hidden lg:block flex-1 max-w-2xl pt-4">
					<div className="flex flex-col gap-2 h-full">
						<div className="flex flex-row gap-2">
							<GraphOne />
							<div className="flex flex-col gap-2 w-80">
								<GraphTwo />
								<GraphThree />
							</div>
						</div>
						<div className="flex flex-row gap-2">
							<GraphFour />
							<GraphFive />
						</div>
					</div>
				</div>
				<div className="absolute top-6 right-10">
					<State />
				</div>
				<div className="md:min-w-xl min-w-[20.5rem] w-[50rem] h-full">
					<ChatContainer />
				</div>
			</div>
		</main>
	);
}
