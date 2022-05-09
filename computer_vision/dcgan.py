import torch.nn as nn

class G(nn.Module): 

    def __init__(self): 
        super(G, self).__init__() 
        self.main = nn.Sequential( 
            nn.ConvTranspose2d(in_channels = 100, out_channels = 512, kernel_size = 4,
                               stride = 1, padding = 0, bias = False), # inversed convolution
            nn.BatchNorm2d(512), # normalize all the features along the dimension of the batch.
            nn.ReLU(True), # inplace is true
            nn.ConvTranspose2d(in_channels = 512, out_channels = 256, kernel_size = 4,
                               stride = 2, padding = 1, bias = False), 
            nn.BatchNorm2d(256), 
            nn.ReLU(True), 
            nn.ConvTranspose2d(in_channels = 256, out_channels = 128, kernel_size = 4,
                               stride = 2, padding = 1, bias = False), 
            nn.BatchNorm2d(128), 
            nn.ReLU(True), 
            nn.ConvTranspose2d(in_channels = 128, out_channels = 64, kernel_size = 4,
                               stride = 2, padding = 1, bias = False), 
            nn.BatchNorm2d(64), 
            nn.ReLU(True), 
            nn.ConvTranspose2d(in_channels = 64, out_channels = 3, kernel_size = 4,
                               stride = 2, padding = 1, bias = False), 
            nn.Tanh() # stay between -1 and +1
        )

    def forward(self, input): 
        output = self.main(input) 
        return output 

class D(nn.Module): 

    def __init__(self): 
        super(D, self).__init__()
        self.main = nn.Sequential( 
            nn.Conv2d(in_channels = 3, out_channels = 64, kernel_size = 4, stride = 2, padding = 1, bias = False), # input channels match the output of the generator
            nn.LeakyReLU(0.2, inplace = True), # negative slope = 0.2, 
            nn.Conv2d(in_channels = 64, out_channels = 128, kernel_size = 4, stride = 2, padding = 1, bias = False),
            nn.BatchNorm2d(128), # normalize all the features along the dimension of the batch.
            nn.LeakyReLU(0.2, inplace = True), 
            nn.Conv2d(in_channels = 128, out_channels = 256, kernel_size = 4, stride = 2, padding = 1, bias = False),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace = True), 
            nn.Conv2d(in_channels = 256, out_channels = 512, kernel_size = 4, stride = 2, padding = 1, bias = False),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2, inplace = True), 
            nn.Conv2d(in_channels = 512, out_channels = 1, kernel_size = 4, stride = 1, padding = 0, bias = False),
            nn.Sigmoid() #  stay between 0 and 1
        )

    def forward(self, input): 
        output = self.main(input) 
        return output.view(-1)