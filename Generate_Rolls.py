import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time


# gets the probability to roll 
# roll_needed or higher
# on at least hits_needed dice
# out of dice_rolled total dice
def Get_Prob(dice_rolled, roll_needed, hits_needed):
    success = np.zeros(samples)  # array of successes to populate
    for i in range(samples):  # loop through all throws
        hits = 0  # start hit counter at 0
        for j in range(dice_rolled):  # loop through dice in a given throw
            if R[j,i] >= roll_needed:  # if it's a hit, add 1 to the hit counter
                hits += 1
        if hits >= hits_needed:  # if we get enough hits, call that roll a success
            success[i] = 1

    return np.mean(success)  # average all successes and failures

# make an array of all probabilities for all desired throws
def Make_Prob_Array():
    # prob_array[dice_rolled, roll_needed_for_hit, hits_needed]
    prob_array = np.zeros((ndice+1, nfaces+1, ndice+1))  # index 0 unused
    for i in range(1, ndice+1):  # dice rolled
        for j in range(1, nfaces+1):  # roll needed
            for k in range(1, i+1):  # hits needed
                prob_array[i, j, k] = Get_Prob(i,j,k)
        print(f'{np.round(i/ndice, 2)*100}% complete')
    return np.round(prob_array*100).astype(int)

def prob_plot(prob_array):
    fsize = 12
    widths = [i for i in range(1,ndice+1)]
    fig, ax = plt.subplots(ncols=ndice, figsize=(ndice*9/2.82,nfaces*2.5/2.82), gridspec_kw={'width_ratios': widths})  # doesnt work for >8 dice
    for dice in range(1, ndice+1):  # loop over all possible number of dice to throw
        arr = prob_array[dice, :, :]  # all probabilities for given number of dice
        col = dice - 1
        # set the aspect ratio so everything is square and nothing is squished
        asp = dice/(nfaces-1)
        ax[col].set_aspect(asp)
        im = ax[col].imshow(arr)  # make a heatmap plot of probabilites in arr
        
        # black magic to put labels inside each cell
        # https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html
        for i in range(2, len(arr[0:nfaces+1, 0])):  # loop over y axis???
            for j in range(1, len(arr[0, 1:dice+1]) + 1):  # loop over x axis???
                text = ax[col].text(j, i, arr[i, j],  # I think this prints the value a[i,j] into the correct cell
                    ha="center", va="center", color="black", fontsize=fsize)  # center text in the cell, text color black
                
                # https://osxastrotricks.wordpress.com/2014/12/02/add-border-around-text-with-matplotlib/
                text.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='white')])  # make text black-on-white for readability
        plt.draw()  # don't know what this does
        
        ax[col].set_title(f"{dice} Dice", fontsize=fsize)  # subplot title
        ax[col].set_xlim([0.5, dice + 0.5])  # cells are centered at integers, so boundaries at half-integer valued
        ax[col].set_ylim([nfaces + 0.5, 1.5])  # same as previous line
        ax[col].set_xticks([i for i in range(1, dice+1)])
        ax[col].set_yticks([])
        ax[col].tick_params(axis='x', labelsize=fsize)

    ax[-1].set_xlabel("Min. # hits desired", fontsize=fsize)  # x axis
    ax[0].set_title("1 Die", fontsize=fsize)  # x axis
    ax[0].set_ylabel("Min. roll to hit", fontsize=fsize)  # y axis
    ax[0].set_xticks([1])
    ax[0].set_yticks([i for i in range(2, nfaces+1)])
    ax[0].tick_params(axis='x', labelsize=fsize)
    ax[0].tick_params(axis='y', labelsize=fsize)

    # black magic to make the colorbar not squish everything
    # https://joseph-long.com/writing/colorbars/
    # divider = make_axes_locatable(ax[-1])
    # cax = divider.append_axes("right", size="10000%", pad=0.1)
    # fig.colorbar(im, cax=cax)
    
    fig.suptitle("Probability of getting at least the desired number of hits given a minimum roll that generates a hit", fontsize=fsize*1.2)
    plt.savefig(f'{ndice}xD{nfaces}.png')
    #plt.show()

if __name__ == '__main__':
    # simulated probability table for the question
    # "Probability to roll X or higher N times with M dice?"
    # simulates up to 8xD6
    for i in range(5):
        nfaces = [4,6,8,12,20][i]
        ndice = [6,8,6,4,4][i]  # roll up to 3
        samples = 500000  # of throws to gather data from
        print(f'{ndice}xD{nfaces}')
        R = np.random.randint(1, nfaces+1, size=(ndice, samples))  # array of random dice rolls
        prob_array = Make_Prob_Array()
        prob_plot(prob_array)
