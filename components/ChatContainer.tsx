"use client";

import { Tooltip } from "chart.js";
import {
	BookKey,
	GaugeCircle,
	History,
	Paperclip,
	PenTool,
	PlusIcon,
	SendIcon,
	SquareMenu,
	ToolCase,
	ToolCaseIcon,
	ChevronDown,
} from "lucide-react";
import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Message {
	id: string;
	text: string;
	isUser: boolean;
	timestamp: Date;
}

function ChatContainer() {
	const [isInputActive, setIsInputActive] = useState(false);
	const [inputValue, setInputValue] = useState("");
	const [messages, setMessages] = useState<Message[]>([]);
	const [isLoading, setIsLoading] = useState(false);
	const [isUserScrolling, setIsUserScrolling] = useState(false);
	const messagesEndRef = useRef<HTMLDivElement>(null);
	const chatContainerRef = useRef<HTMLDivElement>(null);

	const scrollToBottom = () => {
		messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
	};

	const handleScroll = () => {
		if (!chatContainerRef.current) return;

		const { scrollTop, scrollHeight, clientHeight } = chatContainerRef.current;
		const isAtBottom = scrollTop + clientHeight >= scrollHeight - 10;

		setIsUserScrolling(!isAtBottom);
	};

	useEffect(() => {
		// Auto scroll hanya jika user tidak sedang scroll ke atas
		if (!isUserScrolling) {
			scrollToBottom();
		}
	}, [messages, isUserScrolling]);

	const handleContainerClick = () => {
		setIsInputActive(true);
	};

	const handleInputBlur = () => {
		if (inputValue.trim() === "") {
			setIsInputActive(false);
		}
	};

	const handleSendMessage = async () => {
		if (inputValue.trim() === "" || isLoading) return;

		const userMessage: Message = {
			id: Date.now().toString(),
			text: inputValue.trim(),
			isUser: true,
			timestamp: new Date(),
		};

		// Tambahkan pesan user ke chat
		setMessages((prev) => [...prev, userMessage]);
		const currentInput = inputValue.trim();
		setInputValue("");
		setIsLoading(true);
		setIsUserScrolling(false); // Force scroll to bottom when sending message

		// Tambahkan indikator loading
		const loadingMessage: Message = {
			id: "loading",
			text: "Sedang mengetik...",
			isUser: false,
			timestamp: new Date(),
		};
		setMessages((prev) => [...prev, loadingMessage]);

		try {
			// Kirim pesan ke backend
			const apiUrl =
				process.env.NEXT_PUBLIC_CHATBOT_API_URL || "http://10.11.1.207:8012";

			console.log("Sending request to:", apiUrl);
			console.log("Message:", currentInput);

			const response = await fetch(`${apiUrl}/api/chat`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ message: currentInput }),
			});

			console.log("Response status:", response.status);
			console.log("Response ok:", response.ok);

			if (!response.ok) {
				const errorText = await response.text();
				console.error("Error response:", errorText);
				throw new Error(
					`HTTP error! status: ${response.status} - ${errorText}`,
				);
			}

			const data = await response.json();
			console.log("Response data:", data);

			// Hapus pesan loading dan tambahkan respons bot
			setMessages((prev) => {
				const withoutLoading = prev.filter((msg) => msg.id !== "loading");
				const botMessage: Message = {
					id: (Date.now() + 1).toString(),
					text: data.data.response, // Access the nested response field
					isUser: false,
					timestamp: new Date(),
				};
				return [...withoutLoading, botMessage];
			});
		} catch (error) {
			console.error("Error sending message:", error);

			// Hapus pesan loading dan tampilkan pesan error
			setMessages((prev) => {
				const withoutLoading = prev.filter((msg) => msg.id !== "loading");
				const errorMessage: Message = {
					id: (Date.now() + 1).toString(),
					text: "Maaf, terjadi kesalahan saat menghubungi server. Pastikan backend berjalan di port 8012.",
					isUser: false,
					timestamp: new Date(),
				};
				return [...withoutLoading, errorMessage];
			});
		} finally {
			setIsLoading(false);
		}
	};

	const handleKeyPress = (e: React.KeyboardEvent) => {
		if (e.key === "Enter" && !isLoading) {
			handleSendMessage();
		}
	};

	return (
		<main className="h-full w-full p-3">
			<div className="relative container max-w-4xl h-full flex justify-center items-end bg-anti-flash-white-800 shadow-lg rounded-4xl border border-gray-400/50 overflow-hidden">
				<div className="absolute top-4 left-4 z-100">
					<div className="w-8 h-8 bg-anti-flash-white-800 shadow-sm border text-indigo-dye-200/90 border-indigo-dye-200/20 rounded-full flex items-center justify-center transition-all duration-100 ease-in-out hover:border-indigo-dye-400/50 hover:bg-indigo-dye-50 hover:shadow-lg cursor-pointer active:border-emerald-400 active:shadow-emerald-400 active:shadow-xs">
						<PlusIcon className="transition-colors duration-100 hover:text-emerald-950 font-medium active:text-emerald-400 w-3.5 h-3.5" />
					</div>
				</div>
				<div className="absolute top-4 right-4 z-100">
					<div className="w-8 h-8 bg-anti-flash-white-800 shadow-sm border text-indigo-dye-200/90 border-indigo-dye-200/20 rounded-full flex items-center justify-center transition-all duration-100 ease-in-out hover:border-indigo-dye-400/50 hover:bg-indigo-dye-50 hover:shadow-lg cursor-pointer active:border-emerald-400 active:shadow-emerald-400 active:shadow-xs">
						<History className="transition-colors duration-100 hover:text-emerald-950 font-medium active:text-emerald-400 w-3.5 h-3.5" />
					</div>
				</div>

				{messages.length > 0 && (
					<>
						<div
							ref={chatContainerRef}
							onScroll={handleScroll}
							className="absolute bottom-15 left-4 right-4 overflow-y-auto space-y-1.5 flex flex-col scroll-smooth scrollbar-thin"
							style={{
								maxHeight: "calc(100vh - 200px)",
								paddingRight: "8px",
							}}
						>
							<div className="flex-1"></div>
							{messages.map((message) => (
								<div
									key={message.id}
									className={`flex ${
										message.isUser ? "justify-end" : "justify-start"
									}`}
								>
									{message.isUser ? (
										<div className="max-w-xs lg:max-w-sm px-3 py-2 rounded-xl mx-1 bg-tea-green-600 text-emerald-100 rounded-br-xs border border-indigo-dye-400/10">
											<p className="text-xs">{message.text}</p>
											<span className="text-xs mt-1 block text-emerald-100/70">
												{message.timestamp.toLocaleTimeString([], {
													hour: "2-digit",
													minute: "2-digit",
												})}
											</span>
										</div>
									) : (
										<div className="max-w-lg w-full px-4 py-3 mx-1">
											{message.id === "loading" ? (
												<div className="flex items-center space-x-2">
													<div className="flex space-x-1">
														<div className="w-2 h-2 bg-indigo-dye-300 rounded-full animate-bounce"></div>
														<div
															className="w-2 h-2 bg-indigo-dye-300 rounded-full animate-bounce"
															style={{ animationDelay: "0.1s" }}
														></div>
														<div
															className="w-2 h-2 bg-indigo-dye-300 rounded-full animate-bounce"
															style={{ animationDelay: "0.2s" }}
														></div>
													</div>
													<span className="text-xs text-indigo-dye-400 italic">
														{message.text}
													</span>
												</div>
											) : (
												<>
													<div className="prose prose-sm max-w-none text-indigo-dye-500 prose-headings:text-indigo-dye-600 prose-strong:text-indigo-dye-700 prose-code:text-indigo-dye-800 prose-code:bg-indigo-dye-50 prose-pre:bg-indigo-dye-100 prose-blockquote:border-l-indigo-dye-300 prose-a:text-tea-green-600">
														<ReactMarkdown
															remarkPlugins={[remarkGfm]}
															components={{
																p: ({ children }) => (
																	<p className="text-xs mb-2 last:mb-0">
																		{children}
																	</p>
																),
																h1: ({ children }) => (
																	<h1 className="text-sm font-bold mb-2">
																		{children}
																	</h1>
																),
																h2: ({ children }) => (
																	<h2 className="text-xs font-bold mb-2">
																		{children}
																	</h2>
																),
																h3: ({ children }) => (
																	<h3 className="text-xs font-semibold mb-1">
																		{children}
																	</h3>
																),
																code: ({ children, className }) => {
																	const isInline = !className;
																	return isInline ? (
																		<code className="px-1 py-0.5 bg-indigo-dye-100 text-indigo-dye-800 rounded text-xs">
																			{children}
																		</code>
																	) : (
																		<code className={className}>
																			{children}
																		</code>
																	);
																},
																pre: ({ children }) => (
																	<pre className="bg-indigo-dye-100 p-2 rounded-md text-xs overflow-x-auto">
																		{children}
																	</pre>
																),
																ul: ({ children }) => (
																	<ul className="text-xs list-disc ml-4 mb-2">
																		{children}
																	</ul>
																),
																ol: ({ children }) => (
																	<ol className="text-xs list-decimal ml-4 mb-2">
																		{children}
																	</ol>
																),
																li: ({ children }) => (
																	<li className="mb-1">{children}</li>
																),
																blockquote: ({ children }) => (
																	<blockquote className="border-l-2 border-indigo-dye-300 pl-3 text-xs italic mb-2">
																		{children}
																	</blockquote>
																),
															}}
														>
															{message.text}
														</ReactMarkdown>
													</div>
													<span className="text-xs text-indigo-dye-300/70 mt-1 block">
														{message.timestamp.toLocaleTimeString([], {
															hour: "2-digit",
															minute: "2-digit",
														})}
													</span>
												</>
											)}
										</div>
									)}
								</div>
							))}
							<div ref={messagesEndRef} />
						</div>
						<div className="absolute top-0 left-0 right-0 h-12 bg-gradient-to-b from-anti-flash-white-500 to-transparent pointer-events-none z-10"></div>

						{/* Scroll to bottom button */}
						{isUserScrolling && (
							<div className="absolute bottom-24 right-10 z-20 hover:cursor-pointer">
								<button
									onClick={() => {
										setIsUserScrolling(false);
										scrollToBottom();
									}}
									className="w-5 h-5 bg-indigo-dye-500/40 text-white rounded-full shadow-lg flex items-center justify-center hover:bg-indigo-dye-600/80 transition-all duration-200 hover:shadow-xl active:scale-95 hover:cursor-pointer"
									aria-label="Scroll to bottom"
								>
									<ChevronDown className="w-4 h-4" />
								</button>
							</div>
						)}
					</>
				)}

				<div className="container w-full mx-4 mb-4 flex flex-row gap-2 ">
					<div
						className="container w-full bg-anti-flash-white-800 rounded-full flex flex-row gap-3 items-center text-start px-4 py-1 shadow-md border border-indigo-dye-400/30 transition-all duration-300 ease-in-out hover:shadow-lg hover:border-indigo-dye-400/50 cursor-text"
						onClick={handleContainerClick}
					>
						<div className="transition-transform duration-200 ease-in-out hover:scale-110 cursor-pointer active:scale-95">
							<ToolCase className="w-3.5 h-3.5 text-indigo-dye-100 transition-colors duration-200 hover:text-indigo-dye-200 active:text-emerald-400" />
						</div>
						{isInputActive ? (
							<input
								type="text"
								value={inputValue}
								onChange={(e) => setInputValue(e.target.value)}
								onBlur={handleInputBlur}
								onKeyPress={handleKeyPress}
								placeholder={
									isLoading ? "Mengirim pesan..." : "Mau tanya apa?..."
								}
								className="flex-1 bg-transparent outline-none text-indigo-dye-100 placeholder-indigo-dye-100/60 text-xs"
								autoFocus
								disabled={isLoading}
							/>
						) : (
							<span className="flex-1 text-indigo-dye-100/90 select-none text-xs">
								Mau tanya apa?...
							</span>
						)}
					</div>
					<div
						className={`w-13 h-10 md:w-11 bg-anti-flash-white-800 rounded-full text-center items-center flex justify-center shadow-md border border-indigo-dye-400/30 transition-all duration-100 ease-in-out hover:border-indigo-dye-400/50 hover:bg-indigo-dye-50 hover:shadow-lg cursor-pointer active:border-emerald-400 active:shadow-emerald-400 active:shadow-xs ${
							isLoading ? "opacity-50 cursor-not-allowed" : ""
						}`}
						onClick={handleSendMessage}
					>
						{isLoading ? (
							<div className="w-3.5 h-3.5 border-2 border-indigo-dye-200 border-t-transparent rounded-full animate-spin"></div>
						) : (
							<SendIcon className="w-3.5 h-3.5 transition-colors duration-100 hover:text-emerald-950 font-medium active:text-emerald-400" />
						)}
					</div>
				</div>
			</div>
		</main>
	);
}

export default ChatContainer;
